import argparse


def parse_fasta(filename):
    """
    Parses a FASTA file and returns a dictionary with the header as the key and the sequence as the value.

    Args:
        filename (str): The path to the FASTA file.

    Returns:
        dict: A dictionary with the header as the key and the sequence as the value.
    """
    with open(filename, 'r') as f:
        contents = f.read().split('>')[1:]
        data = {}
        for entry in contents:
            lines = entry.split('\n')
            header = lines[0]
            sequence = ''.join(lines[1:])
            sequence = sequence.replace("*", "") if "*" in sequence else sequence
            data[header] = sequence
    return data



def read_mmseqs_cluster_tsv(file_name):
    """
    Read the tsv file from mmseqs2 cluster output
    """

    cluster_info = []
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            cluster_info.append(line.strip().split('\t'))


    assert len(cluster_info[0]) == 2, "The length of the line is not equal to 2"
    return cluster_info


def out_fasta(data, out_file_name):
    """
    Output the fasta file
    """

    with open(out_file_name, 'w') as f:
        for header, sequence in data.items():
            f.write(">" + header + "\n")
            f.write(sequence + "\n")

    return None


def read_selected_cluster_names(file_name):
    """
    Read the selected cluster names
    """

    cluster_names = []
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            cluster_name = line.strip()
            cluster_names.append(cluster_name)

    return cluster_names


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process selected cluster names.')
    parser.add_argument('cluster_names_file', type=str, help='Path to the file containing selected cluster names')
    parser.add_argument('mmseqs_clusters_file', type=str, help='Path to the mmseqs clusters file')
    parser.add_argument('fasta_file', type=str, help='Path to the full fasta file')
    parser.add_argument('output_fasta_file', type=str, help='Path to the output file')
    parser.add_argument('output_cluster_file', type=str, help='Path to the output cluster file')
    args = parser.parse_args()

    # Read selected cluster names
    cluster_names = read_selected_cluster_names(args.cluster_names_file)
    # read the full fasta file
    full_data = parse_fasta(args.fasta_file)

    # Get full sequence names from mmseqs clusters
    cluster_info = read_mmseqs_cluster_tsv(args.mmseqs_clusters_file)


    # select the cluster info
    selected_cluster_info = ["|".join(item) for item in cluster_info if item[0] in cluster_names]
    # remove duplicates
    selected_cluster_info = list(set(selected_cluster_info))
    # recover the original format
    selected_cluster_info = [item.split("|") for item in selected_cluster_info]


    # save the selected cluster info
    with open(args.output_cluster_file, 'w') as f:
        for item in selected_cluster_info:
            f.write(item[0] + "\t" + item[1] + "\n")

    # selected_sequence_ids = [item[1] for item in cluster_info if item[0] in cluster_names]
    # # remove duplicates
    # selected_sequence_ids = list(set(selected_sequence_ids))

    # get output data and save to fasta
    output_data = {}
    for _,sequence_id in selected_cluster_info:
        output_data[sequence_id] = full_data[sequence_id]
    out_fasta(output_data, args.output_fasta_file)

        

if __name__ == '__main__':
    main()


