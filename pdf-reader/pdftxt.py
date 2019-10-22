#le o pdf
import pdftotext

with open("ba89f59a-81cc-4d02-864c-a8ce2df64585.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

# Iterate over all the pages
for page in pdf:
    print(page)
