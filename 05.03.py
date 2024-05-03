import pandas as pd
import requests
import csv
import xml.etree.ElementTree as ET

def fetch_xml_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to fetch XML data from the provided URL.")
        return None

def parse_xml_data(xml_data):
    if xml_data is None:
        print("XML 데이터가 None입니다. 파싱할 수 없습니다.")
        return []

    root = ET.fromstring(xml_data)
    items = root.findall('.//item')
    parsed_data = []
    for item in items:
        ibobprt = item.find('ibobprt').text
        clsgn = item.find('clsgn').text
        vsslNo = item.find('vsslNo').text
        imoNo = item.find('imoNo').text
        vsslKorNm = item.find('vsslKorNm').text
        vsslEngNm = item.find('vsslEngNm').text
        vsslKnd = item.find('vsslKnd').text
        vsslNlty = item.find('vsslNlty').text
        tonEdycSe = item.find('tonEdycSe').text
        intrlGrtg = item.find('intrlGrtg').text
        grtg = item.find('grtg').text
        ntng = item.find('ntng').text
        vsslTotLt = item.find('vsslTotLt').text
        shdth = item.find('shdth').text
        vsslDrft = item.find('vsslDrft').text
        vsslLt = item.find('vsslLt').text
        vsslDp = item.find('vsslDp').text
        brbtSe = item.find('brbtSe').text
        nvgShapCd = item.find('nvgShapCd').text
        nvgShapNm = item.find('nvgShapNm').text
        vsslCnstrDt_element = item.find('vsslCnstrDt')
        vsslCnstrDt = vsslCnstrDt_element.text if vsslCnstrDt_element is not None else ''
        befClsgn = item.find('befClsgn').text

        parsed_data.append([ibobprt, clsgn, vsslNo, imoNo, vsslKorNm, vsslEngNm, vsslKnd, vsslNlty, tonEdycSe,
                            intrlGrtg, grtg, ntng, vsslTotLt, shdth, vsslDrft, vsslLt, vsslDp, brbtSe,
                            nvgShapCd, nvgShapNm, vsslCnstrDt, befClsgn])

    return parsed_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ibobprt', 'clsgn', 'vsslNo', 'imoNo', 'vsslKorNm', 'vsslEngNm', 'vsslKnd', 'vsslNlty', 'tonEdycSe',
                            'intrlGrtg', 'grtg', 'ntng', 'vsslTotLt', 'shdth', 'vsslDrft', 'vsslLt', 'vsslDp', 'brbtSe',
                            'nvgShapCd', 'nvgShapNm', 'vsslCnstrDt', 'befClsgn'])
        csvwriter.writerows(data)

if __name__ == "__main__":
    base_url = "http://apis.data.go.kr/1192000/SicsVsslManp2/Info?serviceKey=r9AolgZapHhLonRnI%2FHempGD7SJBAGfND1saCEcWuKA5VFiFL0BicoX1Tn91NVR0zLvt74D8mPDqNrlfU%2BWi9A%3D%3D&clsgn="
    
    # unique 컬럼에 있는 값들을 읽어옵니다.
    df = pd.read_csv(r"C:\Users\yohann\Desktop\대학생활자료\24년도1학기\종프\코드\Api\ship_portmis_clsgn_daesan.csv",encoding="cp949")  # 여기에 데이터 프레임의 파일명을 넣으세요.
    unique_values = df['unique'].tolist()

    parsed_data_all = []  # 모든 데이터를 저장할 리스트

    # URLs 생성
    urls = [base_url + str(value) for value in unique_values]

    for i, url in enumerate(urls):
        print(f"Processing URL {i+1}/{len(urls)}: {url}")
        xml_data = fetch_xml_data(url)
        if xml_data:
            parsed_data = parse_xml_data(xml_data)
       
            parsed_data_all.extend(parsed_data)
            print(f"XML 데이터를 성공적으로 추가했습니다.")

    # 모든 데이터를 포함한 DataFrame 생성
    all_data_df = pd.DataFrame(parsed_data_all, columns=['ibobprt', 'clsgn', 'vsslNo', 'imoNo', 'vsslKorNm', 'vsslEngNm', 'vsslKnd', 'vsslNlty', 'tonEdycSe',
                            'intrlGrtg', 'grtg', 'ntng', 'vsslTotLt', 'shdth', 'vsslDrft', 'vsslLt', 'vsslDp', 'brbtSe',
                            'nvgShapCd', 'nvgShapNm', 'vsslCnstrDt', 'befClsgn'])

    # 하나의 CSV 파일로 저장
    all_data_df.to_csv("addition_100.csv", index=False, encoding='cp949')
    print("모든 XML 데이터를 하나의 CSV 파일로 성공적으로 저장했습니다.")
