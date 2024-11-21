import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def main():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie", "David"],
            "Age": [25, 30, 35, 40]
        })

    if "selected_rows" not in st.session_state:
        st.session_state.selected_rows = pd.DataFrame(columns=["Name", "Age"])

    df = st.session_state.df.copy()

    # Add a checkbox column to the DataFrame
    df['Select'] = False

    # Display the DataFrame with checkboxes
    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False)
        },
        disabled=["Name", "Age"],
        key="editable_dataframe"
    )

    # Check for changes in the DataFrame
    if not edited_df.equals(df):
        # Get the selected rows
        selected_rows = edited_df[edited_df['Select']]
        
        # Move selected rows to the new table
        st.session_state.selected_rows = pd.concat([st.session_state.selected_rows, selected_rows[["Name", "Age"]]], ignore_index=True)
        
        # Remove selected rows from the original DataFrame
        st.session_state.df = edited_df[~edited_df['Select']].drop(columns=['Select'])

    # Display the selected rows
    st.write("Selected Rows:")
    st.dataframe(st.session_state.selected_rows, hide_index=True)

if __name__ == "__main__":
    main()

# Function to scrape data from the website
def scrape_data():
    cookies = {
        'ak_bmsc': '0E08843E4257240434F033A03D6714DD~000000000000000000000000000000~YAAQSJ42F2yUkS+TAQAAc5QEQBk6tyeodmKbK0+6Uz4uJ6d/3sUD6zZEk5sfq+ZaP84RgD+ji4onlCBFYFbPm1iycFE72h894XCCgh0ZiTRMWZZ/1Yg9WVZfeyFNfvkR6mg3zLN9nSOfADBrWbtFfvP1bfyiB5Rzqywa88H1NTeX2qvUsS9B9IAiTiRPav/KfjSEuSYEioe4jl6pG14gNkwyjK6FAKUJkQX64e3Q9RVFC+plwrylg+Sg89pWKkt0ED/H9gTMe7s6ix9IyQuYrB7Mdu2QKXDogTeTQTH7C+deNFiHQwcy2c3Sj7iB5mIP8dIRWi2Z2a9YwKksra6mtcu51Zg+BeqaY4rEwy6tS65hmF7yfTCJpw5nUn54Ev4=',
        '_ga': 'GA1.2.1749921805.1731945974',
        '_gid': 'GA1.2.739001020.1731945974',
        '_gat': '1',
        '_ga_KFWPDKF16D': 'GS1.2.1731945975.1.1.1731947398.0.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'ak_bmsc=0E08843E4257240434F033A03D6714DD~000000000000000000000000000000~YAAQSJ42F2yUkS+TAQAAc5QEQBk6tyeodmKbK0+6Uz4uJ6d/3sUD6zZEk5sfq+ZaP84RgD+ji4onlCBFYFbPm1iycFE72h894XCCgh0ZiTRMWZZ/1Yg9WVZfeyFNfvkR6mg3zLN9nSOfADBrWbtFfvP1bfyiB5Rzqywa88H1NTeX2qvUsS9B9IAiTiRPav/KfjSEuSYEioe4jl6pG14gNkwyjK6FAKUJkQX64e3Q9RVFC+plwrylg+Sg89pWKkt0ED/H9gTMe7s6ix9IyQuYrB7Mdu2QKXDogTeTQTH7C+deNFiHQwcy2c3Sj7iB5mIP8dIRWi2Z2a9YwKksra6mtcu51Zg+BeqaY4rEwy6tS65hmF7yfTCJpw5nUn54Ev4=; _ga=GA1.2.1749921805.1731945974; _gid=GA1.2.739001020.1731945974; _gat=1; _ga_KFWPDKF16D=GS1.2.1731945975.1.1.1731947398.0.0.0',
        'origin': 'https://a856-cityrecord.nyc.gov',
        'priority': 'u=0, i',
        'referer': 'https://a856-cityrecord.nyc.gov/Section',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    data_data = []
    for i in range(1,5):
        data = {
            'SectionId': '6',
            'SectionName': '\r\n                                                \r\n                                                    \r\n                                                \r\n                                                Procurement\r\n                                            ',
            'NoticeTypeId': '0',
            'PageNumber': f'{i}',
        }

        response = requests.post('https://a856-cityrecord.nyc.gov/Section', cookies=cookies, headers=headers, data=data)

        # test = scrapy.Selector(text=response.text)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all div elements with class 'notice-item'
        notice_items = soup.find_all('div', class_='notice-container')


        for item in notice_items:
            # Extract text from various fields
            # Extract the title
            title = item.find('h1').text.strip()

            # Extract the agency
            agency = item.find('strong').text.strip()

            # Extract the category
            category = item.find('i', class_='fa fa-tag').next_sibling.strip()

            # Extract the description
            description = item.find('p', class_='short-description').text.strip()

            data_data.append({
                'Agency': agency,
                'Title': title,
                'Description': description,
                'Category': category
            })

    return pd.DataFrame(data_data)


# Streamlit app
st.title('NYC City Record Scraper')
#
url = 'https://a856-cityrecord.nyc.gov/Section'
st.write(f"Scraping data from: {url}")
#
if st.button('Scrape Data'):
    df = scrape_data()
    st.write(f"Total records scraped: {len(df)}")
    st.dataframe(df)

    # Optional: Download CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="nyc_city_record_data.csv",
        mime="text/csv",
    )