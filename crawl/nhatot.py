from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import undetected_chromedriver as uc
from unidecode import unidecode
import pandas as pd

def save_partial_data(data):
    df = pd.DataFrame(data)
    df.to_csv('houses_data.csv', index=False, encoding='utf-8-sig', mode='a', header=not pd.io.common.file_exists('houses_data.csv'))
    print("Đã lưu một phần dữ liệu vào houses_data.csv")

for q in range(2,13):
    driver = uc.Chrome()
    house_links = set()
    for i in range(1,101):
        try:
            url = f"https://www.nhatot.com/mua-ban-nha-dat-quan-{q}-tp-ho-chi-minh?page={i}"
            driver.get(url)

            time.sleep(3)


            house_elements = driver.find_elements(By.CSS_SELECTOR, "div.webeqpz a.crd7gu7")
            if not house_elements:
                print(f"Hết dữ liệu ở trang {i}, dừng quét!")
                break

            for house in house_elements:
                link = house.get_attribute("href")
                if link and link.startswith("https"):  # Đảm bảo là link hợp lệ
                    house_links.add(link)  # Thêm vào set (tự động loại bỏ trùng)

        except NoSuchElementException:
            print("Không tìm thấy phần tử phù hợp!")
        except Exception as e:
            print("Lỗi:", str(e))
    house_links = list(house_links)
    print(f"Tìm thấy {len(house_links)} link nhà quận {q}.")


 # Duyệt qua từng link để lấy thông tin chi tiết
    house_data = []
    for index, link in enumerate(house_links):
        try:
            driver.get(link)
            try:
                driver.find_element(By.CLASS_NAME, "aw__s1olmj66").click()
            except Exception as e:
                pass
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 1000);")
            try:    
                driver.find_element(By.CSS_SELECTOR, "div.wj1kuc button").click()
            except Exception as e:
                pass
            details ={}
            details["price"] = driver.find_element(By.CLASS_NAME,'pyhk1dv').text.strip()
            details["address"] = driver.find_element(By.CLASS_NAME, 'bwq0cbs.flex-1').text.strip()
            try:
                label = driver.find_elements(By.CSS_SELECTOR, "div.a4ep88f span")
                value = driver.find_elements(By.CSS_SELECTOR, "strong.a3jfi3v")
                for l,v in zip(label,value):
                    details[unidecode(l.text.strip())]=v.text.strip()
            except Exception as e:
                print("Lỗi:", str(e))

            house_info = {
                "Giá": details.get("price", "N/A"),
                "Địa chỉ": details.get("address", "N/A"),
                "Loại hình nhà ở": details.get("Loai hinh nha o", "N/A"),
                "Diện tích đất": details.get("Dien tich dat", "N/A"),
                "Chiều ngang": details.get("Chieu ngang", "N/A"),
                "Chiều dài": details.get("Chieu dai", "N/A"),
                "Số phòng ngủ": details.get("So phong ngu", "N/A"),
                "Số phòng vệ sinh": details.get("So phong ve sinh", "N/A"),
                "Tổng số tầng": details.get("Tong so tang", "N/A"),
                "Giấy tờ pháp lý": details.get("Giay to phap ly", "N/A")
            }
            house_data.append(house_info)
            print(f"{index + 1}. {house_info}")

        except Exception as e:
            print(f"Lỗi khi truy cập {link}: {str(e)}")

        # Chuyển dữ liệu thành DataFrame và lưu CSV
    df = pd.DataFrame(house_data)
    df.to_csv(f"Quan_{q}.csv", index=False, encoding='utf-8-sig')
    print(df.head())
    driver.quit()