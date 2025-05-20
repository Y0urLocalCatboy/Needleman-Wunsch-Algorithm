import os
from tkinter import *
from tkinter import ttk, filedialog, simpledialog, messagebox
from algorithm import *

root = Tk()
root.title("Multiple Sequence Alignment - Center Star Method created by Gabriel")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sequences = []
missmatch_penalty = StringVar(value="-1")
gap_penalty = StringVar(value="-2")
match_score = StringVar(value="1")

sequence_display = Text(mainframe, width=60, height=15)
sequence_display.grid(column=1, row=1, columnspan=4, sticky=(W, E))

scrollbar = ttk.Scrollbar(mainframe, orient='vertical', command=sequence_display.yview)
scrollbar.grid(column=5, row=1, sticky=(N, S))
sequence_display.configure(yscrollcommand=scrollbar.set)

params_frame = ttk.LabelFrame(mainframe, text="Scoring Parameters", padding="5 5 5 5")
params_frame.grid(column=1, row=2, columnspan=4, sticky=(W, E), pady=10)

ttk.Label(params_frame, text="Match score:").grid(column=1, row=1, sticky=W, padx=5)
ttk.Entry(params_frame, width=7, textvariable=match_score).grid(column=2, row=1, padx=5)

ttk.Label(params_frame, text="Mismatch penalty:").grid(column=3, row=1, sticky=W, padx=5)
ttk.Entry(params_frame, width=7, textvariable=missmatch_penalty).grid(column=4, row=1, padx=5)

ttk.Label(params_frame, text="Gap penalty:").grid(column=5, row=1, sticky=W, padx=5)
ttk.Entry(params_frame, width=7, textvariable=gap_penalty).grid(column=6, row=1, padx=5)


class SequenceInputDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="Enter sequence:").grid(row=0, column=0, sticky=W)
        self.sequence_entry = Text(master, width=40, height=5)
        self.sequence_entry.grid(row=1, column=0, padx=5, pady=5)
        return self.sequence_entry

    def apply(self):
        self.result = self.sequence_entry.get("1.0", END).strip()


def add_sequence_manually():
    """Opens a dialog for manual sequence input"""
    dialog = SequenceInputDialog(root, title="Add Sequence")
    if dialog.result and dialog.result.strip():
        sequence = ''.join(dialog.result.split())
        sequences.append(sequence)
        update_sequence_display()


def load_fasta_file():
    """Loads a FASTA format file and adds the sequence to the list"""
    file_path = filedialog.askopenfilename(
        title="Select FASTA file",
        filetypes=[("FASTA files", "*.fasta *.fa"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "r") as fasta_file:
            lines = fasta_file.readlines()
            sequence = ""
            sequence_name = f"Sequence {len(sequences) + 1}"

            for line in lines:
                if line.startswith(">"):
                    sequence_name = line.strip()[1:]
                else:
                    sequence += line.strip()

            sequences.append(sequence)
            update_sequence_display()

    except Exception as e:
        sequence_display.delete(1.0, END)
        sequence_display.insert(END, f"Error loading FASTA file: {e}")


def update_sequence_display():
    """Update the text widget with current sequences"""
    sequence_display.config(state='normal')
    sequence_display.delete(1.0, END)
    if not sequences:
        sequence_display.insert(END,
                              "No sequences loaded. Please load sequences using the 'Load Sequence' button\nor add manually using 'Add Sequence' button.")
    else:
        sequence_display.insert(END, "Loaded Sequences:\n\n")
        for i, seq in enumerate(sequences, 1):
            sequence_display.insert(END, f"Sequence {i}: {seq}\n")
    sequence_display.config(state='disabled')


def clear_sequences():
    """Clear all loaded sequences"""
    sequences.clear()
    update_sequence_display()


def remove_last_sequence():
    """Remove the last added sequence"""
    if sequences:
        sequences.pop()
        update_sequence_display()


def calculate_sequence_statistics(aligned_sequences):
    """Calculate statistics for aligned sequences"""
    if not aligned_sequences or len(aligned_sequences) < 2:
        return None

    seq_length = len(aligned_sequences[0])
    num_sequences = len(aligned_sequences)
    statistics = {
        'total_length': seq_length,
        'num_sequences': num_sequences,
        'identical_positions': 0,
        'total_gaps': 0,
        'matches': 0,
        'mismatches': 0,
        'gaps': 0,
        'pairwise_stats': [],
        'conservation_by_position': [],
        'gap_distribution': [0] * seq_length
    }

    for pos in range(seq_length):
        chars_at_pos = [seq[pos] for seq in aligned_sequences]
        gaps_at_pos = chars_at_pos.count('-')
        statistics['gap_distribution'][pos] = gaps_at_pos

        unique_chars = set(chars_at_pos) - {'-'}
        if len(unique_chars) == 1:
            statistics['conservation_by_position'].append('+')
        elif len(unique_chars) <= 2:
            statistics['conservation_by_position'].append(':')
        elif len(unique_chars) <= 3:
            statistics['conservation_by_position'].append('.')
        else:
            statistics['conservation_by_position'].append(' ')

    for i in range(num_sequences):
        for j in range(i + 1, num_sequences):
            matches = 0
            mismatches = 0
            gaps = 0

            for pos in range(seq_length):
                if aligned_sequences[i][pos] == '-' or aligned_sequences[j][pos] == '-':
                    gaps += 1
                elif aligned_sequences[i][pos] == aligned_sequences[j][pos]:
                    matches += 1
                else:
                    mismatches += 1

            identity = (matches / seq_length) * 100
            statistics['pairwise_stats'].append({
                'seq1': i + 1,
                'seq2': j + 1,
                'matches': matches,
                'mismatches': mismatches,
                'gaps': gaps,
                'identity': identity
            })

            statistics['matches'] += matches
            statistics['mismatches'] += mismatches
            statistics['gaps'] += gaps

    total_pairs = len(statistics['pairwise_stats'])
    statistics['avg_matches'] = statistics['matches'] / total_pairs
    statistics['avg_mismatches'] = statistics['mismatches'] / total_pairs
    statistics['avg_gaps'] = statistics['gaps'] / total_pairs
    statistics['avg_identity'] = sum(s['identity'] for s in statistics['pairwise_stats']) / total_pairs
    statistics['total_gaps'] = sum(statistics['gap_distribution'])

    statistics['fully_conserved_positions'] = statistics['conservation_by_position'].count('+')
    statistics['strongly_conserved_positions'] = statistics['conservation_by_position'].count(':')
    statistics['weakly_conserved_positions'] = statistics['conservation_by_position'].count('.')

    return statistics


def generate_statistics_report(aligned_sequences, statistics, original_sequences):
    """Generate a stastitscal report of the alignment(s)"""
    filename = "statistics.txt"

    with open(filename, 'w') as f:
        f.write("Multiple Sequence Alignment Statistics\n")
        f.write("=" * 50 + "\n\n")

        f.write("Input sequences:\n")
        f.write("-" * 50 + "\n")
        for i, seq in enumerate(original_sequences, 1):
            f.write(f"Sequence {i} (length: {len(seq)}): {seq}\n")
        f.write("\n")

        f.write("Aligned sequences:\n")
        f.write("-" * 50 + "\n")
        for i, seq in enumerate(aligned_sequences, 1):
            f.write(f"Sequence {i} (length: {len(seq)}): {seq}\n")
        f.write("\n")

        f.write("Overall statistics:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Number of sequences: {statistics['num_sequences']}\n")
        f.write(f"Alignment length: {statistics['total_length']}\n")
        f.write(f"Average sequence identity: {statistics['avg_identity']:.2f}%\n")
        f.write(f"Total gaps: {statistics['total_gaps']}\n")
        f.write(f"Fully conserved positions: {statistics['fully_conserved_positions']}\n")
        f.write(f"Strongly conserved positions: {statistics['strongly_conserved_positions']}\n")
        f.write(f"Weakly conserved positions: {statistics['weakly_conserved_positions']}\n")
        f.write("\n")

        f.write("Pairwise sequence comparisons:\n")
        f.write("-" * 50 + "\n")
        for stat in statistics['pairwise_stats']:
            f.write(f"Sequence {stat['seq1']} vs Sequence {stat['seq2']}:\n")
            f.write(f"  Matches: {stat['matches']}\n")
            f.write(f"  Mismatches: {stat['mismatches']}\n")
            f.write(f"  Gaps: {stat['gaps']}\n")
            f.write(f"  Identity: {stat['identity']:.2f}%\n\n")

        f.write("Conservation pattern:\n")
        f.write("-" * 50 + "\n")
        f.write("Fully conserved means all sequences have the same residue at that position.\n")
        f.write("Strongly conserved means most sequences have the same residue at that position.\n")
        f.write("Weakly conserved means some sequences have the same residue at that position.\n")
        f.write("Key: + = fully conserved, : = strongly conserved, . = weakly conserved\n")

        conservation = ''.join(statistics['conservation_by_position'])
        for i in range(0, len(conservation), 60):
            f.write(f"{i + 1:>4} {conservation[i:i + 60]}\n")
        f.write("\n")

        f.write("Gap distribution:\n")
        f.write("-" * 50 + "\n")
        f.write("Position: Number of gaps\n")
        for pos, gaps in enumerate(statistics['gap_distribution'], 1):
            if gaps > 0:
                f.write(f"Position {pos}: {gaps} gaps\n")

    return filename


def calculate_alignment():
    """Perform the multiple sequence alignment and generate statistics"""
    if len(sequences) < 2:
        sequence_display.delete(1.0, END)
        sequence_display.insert(END, "Please load at least 2 sequences.")
        return

    try:
        original_sequences = sequences.copy()

        aligned_sequences = main(
            sequences,
            int(match_score.get()),
            int(missmatch_penalty.get()),
            int(gap_penalty.get())
        )

        statistics = calculate_sequence_statistics(aligned_sequences)

        if statistics:
            report_file = generate_statistics_report(aligned_sequences, statistics, original_sequences)

            sequence_display.delete(1.0, END)
            sequence_display.insert(END, "Multiple Sequence Alignment Results:\n\n")

            max_num_width = len(str(len(aligned_sequences)))
            for i, seq in enumerate(aligned_sequences, 1):
                sequence_display.insert(END, f"Sequence {i:{max_num_width}}: {seq}\n")

            sequence_display.insert(END, f"\nBasic Statistics:\n")
            sequence_display.insert(END, f"Average sequence identity: {statistics['avg_identity']:.2f}%\n")
            sequence_display.insert(END, f"Total gaps: {statistics['total_gaps']}\n")
            sequence_display.insert(END, f"Fully conserved positions: {statistics['fully_conserved_positions']}\n")

            messagebox.showinfo("Success",
                                f"Alignment complete!\nDetailed statistics have been saved to:\n{os.path.abspath(report_file)}")

    except ValueError as e:
        sequence_display.delete(1.0, END)
        sequence_display.insert(END, f"Error: {str(e)}")


button_frame = ttk.Frame(mainframe)
button_frame.grid(column=1, row=3, columnspan=4, sticky=(W, E), pady=10)

ttk.Button(button_frame, text="Load From File",
           command=load_fasta_file).grid(column=1, row=1, padx=5)

ttk.Button(button_frame, text="Add Sequence",
           command=add_sequence_manually).grid(column=2, row=1, padx=5)

ttk.Button(button_frame, text="Remove Last",
           command=remove_last_sequence).grid(column=3, row=1, padx=5)

ttk.Button(button_frame, text="Clear All",
           command=clear_sequences).grid(column=4, row=1, padx=5)

ttk.Button(button_frame, text="Calculate Alignment",
           command=calculate_alignment).grid(column=5, row=1, padx=5)

status_label = ttk.Label(mainframe, text="Ready to load sequences")
status_label.grid(column=1, row=4, columnspan=4, sticky=(W, E), pady=5)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

update_sequence_display()

root.mainloop()