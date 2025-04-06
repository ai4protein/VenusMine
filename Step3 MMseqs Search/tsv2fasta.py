import argparse

def read_tsv(file_name):
    """
    Read the tsv file from mmseqs2 cluster output
    :param file_name: the file name
    :return: a list of lists
    """

    seq_info_list = []
    header = ["query","target","pident","fident","nident","alnlen","bits","tseq","evalue"]
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            seq_info = line.strip().split('\t')
            seq_info_list.append(seq_info)


    assert len(seq_info_list[0]) == len(header), "The length of the header is not equal to the length of the line"
    return header, seq_info_list


def out_fasta(header, seq_info_list, out_file_name, evalue=1e-5):
    """
    Output the fasta file
    """
    tag_index = header.index("target")
    seq_index = header.index("tseq")
    evalue_index = header.index("evalue")

    if evalue is None:
        with open(out_file_name, 'w') as f:
            for seq_info in seq_info_list:
                f.write(">" + seq_info[tag_index] + "\n")
                f.write(seq_info[seq_index] + "\n")
    else:
        with open(out_file_name, 'w') as f:
            for seq_info in seq_info_list:
                if seq_info[evalue_index] <= evalue:
                    f.write(">" + seq_info[tag_index] + "\n")
                    f.write(seq_info[seq_index] + "\n")

    return None


    
def main(input_file, output_file):
    header, data = read_tsv(input_file)
    print("Load the tsv file successfully, length: ", len(data))
    out_fasta(header, data, output_file, evalue=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process some TSV and output to FASTA.",
        usage="python %(prog)s <input_file> <output_file>"
    )
    parser.add_argument('input_file', type=str, help='Input TSV file')
    parser.add_argument('output_file', type=str, help='Output FASTA file')

    args = parser.parse_args()
    main(args.input_file, args.output_file)

