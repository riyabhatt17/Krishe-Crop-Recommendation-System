
# कृShe: Crop Recommendation System 🌾

**कृShe** is a web-based application designed to help farmers make data-driven decisions for optimal crop selection. By analyzing key environmental parameters such as soil composition, climate conditions, and historical data, the application predicts the most suitable crop for specific conditions, promoting sustainable agriculture and optimizing yields.

---

## Features ✨

- **User Registration and Login System**  
  Secure user authentication and account management.
  
- **Crop Recommendation**  
  Predicts suitable crops based on environmental parameters.

- **Data Visualization and Analysis**  
  Presents insights for better decision-making.

- **User-Friendly Interface**  
  Seamlessly designed with Bootstrap for an intuitive user experience.

---

## Project Structure 📂

```
.
├── app.py
├── Crop Classification With Recommendation System.ipynb
├── Crop_recommendation.csv
├── instance/
├── minmaxscaler.pkl
├── model.pkl
├── my_new_env/
├── standscaler.pkl
├── static/
│   ├── img.jpg
│   ├── new.jpg
│   ├── about1.jpg
├── templates/
│   ├── about.html
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── team.html
│   ├── chatbot.html

```

---

## Installation ⚙️

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/jyoti-131/krishe.git
   cd krishe
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv my_new_env
   source my_new_env/bin/activate  # On Windows use `my_new_env\Scripts\activate`
   ```

3. **Install the Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

5. **Run the Application:**
   ```bash
   flask run
   ```

---

## Usage 🖥️

- **Home Page:**  
  Provides an overview of the application and its features.

- **Register:**  
  New users can register by providing a username, email, and password.

- **Login:**  
  Registered users can log in using their credentials.

- **Predict:**  
  Users can input environmental parameters (Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall) to get crop recommendations.

- **About Us:**  
  Learn about the mission and benefits of using कृShe.

---

## Data 📊

The dataset used for training the model is `Crop_recommendation.csv`, containing the following columns:

| **Column**       | **Description**                              |
|-------------------|----------------------------------------------|
| `N`              | Nitrogen content in the soil                 |
| `P`              | Phosphorus content in the soil               |
| `K`              | Potassium content in the soil                |
| `temperature`    | Temperature in degrees Celsius               |
| `humidity`       | Relative humidity in percentage              |
| `ph`             | pH value of the soil                         |
| `rainfall`       | Rainfall in mm                               |
| `label`          | Crop label                                   |

---

## Contributing 🤝

Feel free to fork the repository and make contributions. Pull requests are welcome!

---

## License 📜

This project is licensed.

---
