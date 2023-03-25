from filecmp import dircmp
import difflib


def print_diff_files(dcmp, print_file_differences):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
        if print_file_differences:
            print("The only difference in files are:")
            with open(dcmp.left + "\\" + name) as file_1:
                file_1_text = file_1.readlines()

            with open(dcmp.right + "\\" + name) as file_2:
                file_2_text = file_2.readlines()

            # Find and print the diff:
            for line in difflib.unified_diff(
                file_1_text,
                file_2_text,
                fromfile=dcmp.left + "\\" + name,
                tofile=dcmp.right + "\\" + name,
                lineterm="",
            ):
                print(line)

    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp, print_file_differences)


def print_diff_text_in_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))

    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


folder_1 = "V1"
folder_2 = "V2"
dcmp = dircmp(folder_1, folder_2)
print("The only files with differences are:")
print_diff_files(dcmp, False)
input("You can have manual check of the files  too")
print("The only files with differences and their differences are:")
print_diff_files(dcmp, True)
