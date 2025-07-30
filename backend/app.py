from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)


PATH_FILE_DATA = "/home/thaiv7/Desktop/python-project/scientific_paper/dataset/data/arxiv_metadata_filtered.parquet"

df = pd.read_parquet(PATH_FILE_DATA)

@app.route('/data', methods=['GET'])
def get_data():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    year = request.args.get('year')
    categories = request.args.getlist('category') # can be multiple categories

    print(f"Categories: {categories}, Year: {year}, Page: {page}, Size: {size}")
    for cat in categories:
        print(f"Category: {cat}")

    filtered_df = df.copy()
    if year:
        filtered_df = filtered_df[filtered_df['update_date'].str.startswith(year)]

    if categories:
        filtered_df = filtered_df[filtered_df['categories'].apply(
            lambda cat_str: any(cat in cat_str.split(' ') for cat in categories)
        )]

    total_rows = len(filtered_df)
    total_pages = (total_rows + size - 1) // size
    start = (page - 1) * size
    end = start + size

    sliced_df = filtered_df.iloc[start:end]

    return jsonify({
        'data': sliced_df.to_dict(orient='records'),
        'total_pages': total_pages,
        'current_page': page,
        'total_rows': total_rows
    })

if __name__ == '__main__':
    app.run(debug=True)
