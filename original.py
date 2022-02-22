import csv


def read_site_company(filename):
    with open(filename, newline='') as csvfile:
        siteCompany = {}

        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        # skip first row
        firstRow = next(fileReader)

        for row in fileReader:
            siteCompany[row[1]] = row[3]
    
    return siteCompany
        

def read_file(filename, siteCompany):
    # column mappings:
    # Company name -> newRow[1]
    # Volume -> newRow[2]
    # Year -> newRow[3]
    # Month -> newRow[4]

    with open(filename, newline='') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        currentRow = ['', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        newRows = []

        # skip first row
        firstRow = next(fileReader)

        for newRow in fileReader:
            year = int(newRow[3])
            month = int(newRow[4])
            volume = int(newRow[2])
            try:
                company = siteCompany[newRow[1]]
            except KeyError:
                print(f"Site {newRow[1]} not found in company mapping")

            # check if we're at a new company
            # if we are, then append currentRow to newRows []
            # and reset currentRow
            if company != currentRow[0]:
                # append currentRow to newRows[] only if currentRow[0] != ''
                if currentRow[0] != '':
                    newRows.append(currentRow)

                # reset currentRow
                currentRow = [company, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            # if 2022 (Jan), then it's our 13th column
            if year == 2022:
                month = 13

            currentRow[month] += volume

            # add total volume
            currentRow[14] += volume

        newRows.append(currentRow)
        csvfile.close()

        return newRows


def write_file(filename, data):
    with open(filename, "w+", newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerows(output)
        csvFile.flush()
        csvFile.close()


# main routine
if __name__ == '__main__':
    siteCompanyFile = "site_company.csv"
    siteCompany = read_site_company(siteCompanyFile)
    inputFile = 'send_volumes_month.csv'
    output = read_file(inputFile, siteCompany)
    outputFile = 'results.csv'
    write_file(outputFile, output)
