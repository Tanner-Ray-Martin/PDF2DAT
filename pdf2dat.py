from app.core import pdf_to_dat



for pdf_path in pdf_to_dat.get_new_pdfs():
    print(pdf_path)
    pdf = pdf_to_dat.load_pdf(pdf_path)
    for page in pdf.pages:
        page_data = pdf_to_dat.get_page_text(page)
        for idx, line_of_text in enumerate(page_data):
            if pdf_to_dat.is_dimension_location_line(line_of_text):
                dimension_location = pdf_to_dat.get_dimension_location_from_line(line_of_text)
                dimension_location_values_text = page_data[idx+1]
                dimension_location_data = pdf_to_dat.convert_dimension_text_2_object(dimension_location_values_text)
                fomrmatted_location_data = pdf_to_dat.format_dimension_float_as_dat(dimension_location_data)
                location_dat_file_text = pdf_to_dat.create_dat_file_text(dimension_location, fomrmatted_location_data)
                saved_dat_file_path = pdf_to_dat.save_text_to_dat_file_and_return_path(dimension_location, location_dat_file_text)
                print(saved_dat_file_path)
    pdf_to_dat.move_pdf(pdf_path)