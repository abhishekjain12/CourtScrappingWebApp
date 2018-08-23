# fw = open(module_directory + "/../Data_Files/Html_Files/" + court_name + "_" +
#           str(start_date).replace("/", "-") + "_" + str(i) + ".html", "w")
# fw.write(str(res))
import glob
import shutil


def file_transfer_to_bucket():
    while True:
        for filename in glob.glob("/home/karaa_krypt/CourtScrappingWebApp/Data_Files/JSON_Files/*.json"):
            shutil.copy(filename, "/home/karaa_krypt/bucket_dir/JSON_Files")

        for filename in glob.glob("/home/karaa_krypt/CourtScrappingWebApp/Data_Files/PDF_Files/*.pdf"):
            shutil.copy(filename, "/home/karaa_krypt/bucket_dir/PDF_Files")

        for filename in glob.glob("/home/karaa_krypt/CourtScrappingWebApp/Data_Files/Text_Files/*.txt"):
            shutil.copy(filename, "/home/karaa_krypt/bucket_dir/Text_Files")
