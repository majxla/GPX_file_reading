import xml.etree.ElementTree as et
import sys


ns = {
    '': 'http://www.topografix.com/GPX/1/1'
}


def main():
    #file_name = './pd2/Katalog z przykładowymi plikami GPX-20240122/lublin-siedlce-warszawa.gpx'
    #file_name = './pd2/Katalog z przykładowymi plikami GPX-20240122/example.gpx'
    
    file_name = input("GPX file absolute path: ")

    highest_point = None
    highest_point_coords = None
    lowest_point = None
    lowest_point_coords = None

    bounding_box = {'min_lon': None, 'min_lat': None, 'max_lon': None, 'max_lat': None}

    try:
        gpx_doc = et.parse(file_name)
        gpx = gpx_doc.getroot()
        trk = gpx.find('trk', ns)

        sum_of_ele = 0

        for trkseg in trk.findall('trkseg', ns):

            sum_of_ele_seg = 0

            trkpts = trkseg.findall('trkpt', ns)
            for i, trkpt in enumerate(trkpts):

                try:
                    ele = float(trkpt.find('ele', ns).text)

                    try:
                        # sum of elevation 
                        # only those pairs of points are taken into account for which the height of both is given and the height of the the second is higher than the first
                        next_ele = float(trkpts[i+1].find('ele', ns).text)
                        
                        if ele < next_ele:
                            sum_of_ele_seg += next_ele - ele

                    except IndexError:
                        pass
                    
                    trkpt_lon = float(trkpt.attrib['lon'])
                    trkpt_lat = float(trkpt.attrib['lat'])

                    # lowest and highest point
                    if highest_point == None or highest_point < ele:
                        highest_point = ele
                        highest_point_coords = (trkpt_lat, trkpt_lon)
                    if lowest_point == None or lowest_point > ele:
                        lowest_point = ele
                        lowest_point_coords = (trkpt_lat, trkpt_lon)
                    
                    # bouding box
                    if bounding_box['min_lon'] == None or trkpt_lon < bounding_box['min_lon']:
                        bounding_box['min_lon'] = trkpt_lon

                    if bounding_box['min_lat'] == None or trkpt_lat < bounding_box['min_lat']:
                        bounding_box['min_lat'] = trkpt_lat

                    if bounding_box['max_lon'] == None or trkpt_lon > bounding_box['max_lon']:
                        bounding_box['max_lon'] = trkpt_lon
                    
                    if bounding_box['max_lat'] == None or trkpt_lat > bounding_box['max_lat']:
                        bounding_box['max_lat'] = trkpt_lat
                    
                    
                except AttributeError:
                    sys.exit("File does not contain elevation information.")
            
            sum_of_ele += sum_of_ele_seg
        
        # zaokrąglić do jednego miejsca po przecinku
        print(f'--Total elevation for the entire route: {sum_of_ele:.1f}')
        print()
        print(f'--Bounding Box\n min_lon: {bounding_box["min_lon"]},\n min_lat: {bounding_box["min_lat"]},\n max_lon: {bounding_box["max_lon"]},\n max_lat: {bounding_box["max_lat"]}')
        print()
        print(f'--Highest point\nlat: {highest_point_coords[0]}, lon: {highest_point_coords[0]}\nelevation: {highest_point}')
        print()
        print(f'--Lowest point\nlat: {lowest_point_coords[0]}, lon: {lowest_point_coords[0]}\nelevation: {lowest_point}')
        

    except FileNotFoundError:
        sys.exit("File not found.")


if __name__ == "__main__":
    main()