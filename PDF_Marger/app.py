from PyPDF2 import PdfMerger

def merge_pdfs(pdf1_path, pdf2_path, output_path):
    merger = PdfMerger()
    
    # Append the PDF files
    merger.append(pdf1_path)
    merger.append(pdf2_path)
    
    # Write out the merged PDF
    merger.write(output_path)
    merger.close()
    print(f"Merged PDF saved as: {output_path}")

# Example usage
merge_pdfs("file1.pdf", "file2.pdf", "merged_output.pdf")
