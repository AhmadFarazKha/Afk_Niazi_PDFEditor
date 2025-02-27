import streamlit as st
import fitz  # PyMuPDF for PDF manipulation
import pdfplumber
from io import BytesIO
from reportlab.pdfgen import canvas
from streamlit_pdf_viewer import pdf_viewer

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Afk_Niazi PDF Editor", layout="wide")
st.markdown("<h1 style='text-align: center; color: #007BFF;'>📄 Afk_Niazi PDF Editor 🚀</h1>", unsafe_allow_html=True)

# ---- SIDEBAR ----
option = st.sidebar.radio("Choose an Operation", 
                          ["📝 Edit PDF", "📑 Merge PDFs", "🌊 Add Watermark", "🔄 Rotate PDF", "✂️ Split PDF"])

# ---- PDF EDITOR ----
if option == "📝 Edit PDF":
    st.subheader("Edit Your PDF Live")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"

        pdf_bytes = uploaded_file.read()
        st.info("📄 PDF Preview Below:")
        pdf_viewer(pdf_bytes)

        # Text Editor
        edited_text = st.text_area("Modify Text", text, height=300)

        # Save Edited PDF
        if st.button("Save Edited PDF"):
            output = BytesIO()
            c = canvas.Canvas(output)
            c.drawString(100, 750, edited_text)
            c.save()
            output.seek(0)
            
            st.download_button("📥 Download Edited PDF", data=output, file_name="edited.pdf", mime="application/pdf")

# ---- MERGE PDFs ----
elif option == "📑 Merge PDFs":
    st.subheader("Merge Multiple PDFs")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    if uploaded_files and st.button("Merge PDFs"):
        merger = fitz.open()
        for pdf in uploaded_files:
            merger.insert_pdf(fitz.open(pdf))

        merged_pdf = BytesIO()
        merger.save(merged_pdf)
        merged_pdf.seek(0)

        st.success("✅ PDFs Merged Successfully!")
        st.download_button("📥 Download Merged PDF", data=merged_pdf, file_name="merged.pdf", mime="application/pdf")

# ---- WATERMARK PDFs ----
elif option == "🌊 Add Watermark":
    st.subheader("Add Watermark to a PDF")
    main_pdf = st.file_uploader("Upload Main PDF", type="pdf", key="main")
    watermark_text = st.text_input("Enter Watermark Text")

    if main_pdf and watermark_text and st.button("Apply Watermark"):
        doc = fitz.open(stream=main_pdf.read(), filetype="pdf")

        for page in doc:
            rect = page.rect
            page.insert_text((rect.width / 2 - 50, rect.height / 2), watermark_text, fontsize=20, color=(0.6, 0.6, 0.6))

        watermarked_pdf = BytesIO()
        doc.save(watermarked_pdf)
        doc.close()
        watermarked_pdf.seek(0)

        st.success("✅ Watermark Added Successfully!")
        st.download_button("📥 Download Watermarked PDF", data=watermarked_pdf, file_name="watermarked.pdf", mime="application/pdf")

# ---- ROTATE PDFs ----
elif option == "🔄 Rotate PDF":
    st.subheader("Rotate a PDF")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    rotation_angle = st.selectbox("Select Rotation Angle", [90, 180, 270])

    if uploaded_file and st.button("Rotate PDF"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        for page in doc:
            page.set_rotation(rotation_angle)

        rotated_pdf = BytesIO()
        doc.save(rotated_pdf)
        doc.close()
        rotated_pdf.seek(0)

        st.success(f"✅ PDF Rotated {rotation_angle}° Successfully!")
        st.download_button("📥 Download Rotated PDF", data=rotated_pdf, file_name="rotated.pdf", mime="application/pdf")

# ---- SPLIT PDFs ----
elif option == "✂️ Split PDF":
    st.subheader("Split PDF into Individual Pages")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file and st.button("Split PDF"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, page in enumerate(doc):
                single_page_pdf = fitz.open()
                single_page_pdf.insert_pdf(doc, from_page=i, to_page=i)
                pdf_bytes = single_page_pdf.write()
                zip_file.writestr(f"page_{i+1}.pdf", pdf_bytes)

        zip_buffer.seek(0)

        st.success("✅ PDF Split Successfully!")
        st.download_button("📥 Download Split PDFs (ZIP)", data=zip_buffer, file_name="split_pages.zip", mime="application/zip")
