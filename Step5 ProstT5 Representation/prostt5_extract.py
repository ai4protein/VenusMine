from transformers import T5Tokenizer, T5EncoderModel
import torch
import numpy as np
import time
import pickle
import glob
import os
import logging
import argparse


SEQ_THRESHOLD = 1000  # Change this value if you want to set a different threshold
BATCH_SIZE = 1  # Set the batch size
CUDA_DEVICE = 'cuda:0'  # Choose which CUDA device to use


# Parses fasta file and returns sequence header and sequence in a list
def parse_fasta(filename):
    with open(filename, 'r') as f:
        contents = f.read().split('>')[1:]
        data = []
        for entry in contents:
            lines = entry.split('\n')
            header = lines[0]
            sequence = ''.join(lines[1:])
            sequence = sequence.replace("*", "") if "*" in sequence else sequence
            if len(sequence) <= SEQ_THRESHOLD and all(aa in 'ACDEFGHIKLMNPQRSTVWY' for aa in sequence):
                data.append((header, sequence))
    return data


# Returns sequence labels, sequences, and their ESM representations
def calculate_representation(model, tokenizer, data, device, logger, start_time):

    sequence_labels, sequence_strs, sequence_representations = [], [], []
    total_sequences, num_batches = len(data), len(data) // BATCH_SIZE + (len(data) % BATCH_SIZE != 0)

    for batch in range(num_batches):
        start_idx, end_idx = batch * BATCH_SIZE, (batch + 1) * BATCH_SIZE
        if end_idx > total_sequences:
            end_idx = total_sequences

        batch_labels = []
        batch_strs = []
        batch_strs_model = []

        for i in range(start_idx, end_idx):
            batch_labels.append(data[i][0])
            batch_strs.append(data[i][1])
            if data[i][1].isupper():
                batch_strs_model.append("<AA2fold>" + " " + " ".join(list(data[i][1])))
            else:
                batch_strs_model.append("<fold2AA>" + " " + " ".join(list(data[i][1])))



        # tokenize sequences and pad up to the longest sequence in the batch
        ids = tokenizer.batch_encode_plus(batch_strs_model, add_special_tokens=True, padding="longest",return_tensors='pt').to(device)

        # generate embeddings
        with torch.no_grad():
            token_representations = model(
                                    ids.input_ids, 
                                    attention_mask=ids.attention_mask
                                    )
        

        for i in range(len(batch_strs)):
            sequence_representations.append(token_representations.last_hidden_state[i,1:len(batch_strs[i])+1].mean(dim=0).cpu().numpy())
            sequence_labels.append(batch_labels[i])
            sequence_strs.append(batch_strs[i])

        logger.info(f"Batch {batch + 1}/{num_batches} processed in {time.time() - start_time} seconds. Progress: {100.0 * (batch + 1) / num_batches:.2f}%")

        del batch_labels, batch_strs, batch_strs_model, token_representations
        torch.cuda.empty_cache()

    return sequence_labels, sequence_strs, np.vstack(sequence_representations)


# Saves the representation, sequence labels, and sequences to a pickle file
def save_representation(sequence_labels, sequence_strs, representation, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump({"labels": sequence_labels, "sequences": sequence_strs, "representations": representation}, f)


def main(input_files_pattern, output_dir, log_file):
    # Setting up logging
    logging.basicConfig(filename=log_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    start_time = time.time()
    
    device = CUDA_DEVICE if torch.cuda.is_available() else 'cpu'
    logger.info(f"Device: {device}")

    tokenizer = T5Tokenizer.from_pretrained('Rostlab/ProstT5', do_lower_case=False)
    model = T5EncoderModel.from_pretrained("Rostlab/ProstT5").to(device)
    # only GPUs support half-precision currently; if you want to run on CPU use full-precision (not recommended, much slower)
    model.full() if device=='cpu' else model.half()


    input_files = glob.glob(input_files_pattern)
    
    for input_file in input_files:
        data = parse_fasta(input_file)
        logger.info(f"Read {len(data)} sequences from {input_file}.")

        sequence_labels, sequence_strs, representation = calculate_representation(model, tokenizer, data, device, logger, start_time)

        output_filename = os.path.splitext(os.path.basename(input_file))[0] + '.pkl'
        output_file = os.path.join(output_dir, output_filename)

        save_representation(sequence_labels, sequence_strs, representation, output_file)

    logger.info(f"Total time taken: {time.time() - start_time}  seconds")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute representations for protein sequences.')
    parser.add_argument('input_files_pattern', type=str, help='Input pattern to match fasta files.')
    parser.add_argument('output_dir', type=str, help='Output directory to save representations.')
    parser.add_argument('--log_file', type=str, default='repr_extract.log', help='Path to save the log file.')

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        print(f"Error: Output directory '{args.output_dir}' does not exist!")
        print(f"Given input: {args}")
        exit(1)
    
    main(args.input_files_pattern, args.output_dir, args.log_file)




