# BizCardX: Extracting Business Card Data with OCR

BizCardX is an innovative project aimed at simplifying the process of managing business card data by leveraging Optical Character Recognition (OCR) technology. This README provides an overview of the project, installation instructions, and guidance on usage.

## Approach

1. **Install Required Packages**: Ensure you have Python installed along with the necessary packages including Streamlit, easyOCR, and a database management system like SQLite or MySQL.

2. **Design User Interface**: Create a user-friendly interface using Streamlit, guiding users through the process of uploading business card images and extracting information. Utilize widgets such as file uploaders, buttons, and text boxes to enhance interactivity.

3. **Implement Image Processing and OCR**: Utilize easyOCR to extract pertinent information from uploaded business card images. Apply image processing techniques like resizing, cropping, and thresholding to improve image quality before passing it to the OCR engine.

4. **Display Extracted Information**: Present the extracted information in a clean and organized manner within the Streamlit GUI. Utilize widgets like tables, text boxes, and labels for effective presentation.

5. **Implement Database Integration**: Integrate a database management system such as SQLite or MySQL to store extracted information alongside uploaded business card images. Utilize SQL queries for table creation, data insertion, retrieval, updating, and deletion via the Streamlit UI.

6. **Test the Application**: Thoroughly test the application to ensure proper functionality. Run the application locally using the command `streamlit run app.py` in the terminal, replacing `app.py` with the name of your Streamlit application file.

7. **Continuous Improvement**: Continuously enhance the application by adding new features, optimizing code, and resolving bugs.

## Usage

To run the application:

1. Install Python and required packages by running:

    ```bash
    pip install streamlit easyocr
    ```

2. Ensure you have a database management system installed (e.g., SQLite or MySQL).

3. Clone the project repository:

    ```bash
    git clone https://github.com/your_username/BizCardX.git
    cd BizCardX
    ```

4. Run the application:

    ```bash
    streamlit run app.py
    ```

5. Access the application through your web browser at the provided URL.

## Contributors

- John Doe (@johndoe)
- Jane Smith (@janesmith)

## License

This project is licensed under the [MIT License](LICENSE).
