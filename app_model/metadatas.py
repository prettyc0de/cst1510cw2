def migrate_datsets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn)   


    def get_all_datasets_metadata(conn):
    sql = 'Select * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)
