## Address Extraction Program

The Address Extraction Program is a Python script that extracts address information from websites. It utilizes web scraping techniques to locate specific HTML elements containing address details and saves them to a CSV file. This program is designed to automate the process of gathering address information from multiple websites efficiently.

### Prerequisites

To run the Address Extraction Program, ensure that you have the following dependencies installed:

- Python 3.x
- pandas
- requests
- BeautifulSoup

You can install these dependencies using `pip`, the package installer for Python.

```shell
pip install pandas requests beautifulsoup4
```

### Program Flow

1. **Input Data**: The program takes a list of websites as input, stored in a Parquet file named `websites.parquet`. Each website entry contains the domain name.

2. **Address Extraction**: The program extracts address information by visiting specific web pages of each website. It searches for HTML elements containing address details using class names associated with address components like country, region, city, postcode, road, and road numbers. The web scraping is done using the `requests` and `BeautifulSoup` libraries.

3. **Processing Websites**: The program processes each website entry by iterating through a predefined set of subdomains. It constructs the complete URL by joining the website's domain with each subdomain and extracts the address information from the corresponding web page.

4. **Error Handling**: If no address information is found for a website, the program attempts to fetch the main page content. If an error occurs during the request, the error code is recorded.

5. **Output**: The program collects the extracted address information and any encountered errors for each website. The address details are saved in a CSV file named `addresses.csv`, and the errors are saved in a separate CSV file named `errors.csv`.

### Usage

1. Place the Parquet file `websites.parquet` containing the list of websites in the same directory as the script.

2. Run the script by executing the following command:

```shell
python main.py
```

3. The script will process the websites, extract address information, and save the results to the `addresses.csv` file. Any errors encountered during the process will be saved in the `errors.csv` file.

### Limitations

- The program currently processes a limited number of websites for testing purposes. To process all websites in the input file, remove the line `df = df.head(5)` from the `main` function.

- The program assumes that the address information is located within specific HTML elements and can be identified using class names. Adjustments may be needed for websites with different HTML structures or class names.

- The program relies on the availability and accessibility of the websites. If a website is down or inaccessible, the program will record an error.

### Future Improvements (Multiprocessing)

1. **Improved Performance**: The program currently processes websites sequentially, meaning it processes one website at a time. By introducing multiprocessing, you can leverage the power of multiple CPU cores to process multiple websites simultaneously. This can significantly improve the overall performance and reduce the execution time of the program, especially when dealing with a large number of websites.

2. **Increased Efficiency**: With multiprocessing, the program can take full advantage of the available system resources and distribute the workload across multiple processes. This can lead to better resource utilization and increased efficiency in processing the websites.

3. **Scalability**: Multiprocessing allows the program to scale and handle a larger number of websites efficiently. As the number of websites increases, multiprocessing enables parallel processing, ensuring that each website is processed concurrently, resulting in faster execution times.

Overall, adding multiprocessing to the program can significantly enhance its performance, efficiency, and scalability, providing a more responsive and adaptable solution for processing websites.

### Problems I've ran into

1. AI Language Detect - Implementing an AI Language Detector for the program can be challenging due to the complexity of Natural Language Processing (NLP) and the inherent variability and ambiguity in language. Developing an accurate language detector requires expertise in linguistic patterns, statistical models, and machine learning algorithms. 

2. Multiprocessing - Coordinating multiple processes and managing inter-process communication adds complexity to the program's logic. Additionally, the effectiveness of multiprocessing relies on the availability of sufficient computational resources, such as CPU cores, memory, and I/O bandwidth.

### Conclusion

The Address Extraction Program simplifies the task of extracting address information from websites. By automating the web scraping process, it provides a convenient and efficient solution for gathering address data from multiple websites. This program can be useful for various applications, such as data analysis, data enrichment, and research.

Feel free to use, modify, and enhance the program according to your specific requirements.
