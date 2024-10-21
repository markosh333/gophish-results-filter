import argparse
import csv


email_sent = []
email_opened = []
clicked_link = []
submitted_data = []
email_reported = []

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-f", "--filter", action="store_true")
parser.add_argument("-o", "--output")


def get_data_from_file(file):
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if row[3] == "Email Sent":
                email_sent.append(row[1])
            elif row[3] == "Email Opened":
                email_opened.append(row[1])
            elif row[3] == "Clicked Link":
                clicked_link.append(row[1])
            elif row[3] == "Submitted Data":
                submitted_data.append(row[1])
            elif row[3] == "Email Reported":
                email_reported.append(row[1])


def remove_duplicate_users(users_list):
    return list(dict.fromkeys(users_list))


def remove_spam_filter_noise(users_list):
    tmp = []

    for user in users_list:
        if users_list.count(user) > 1:
            tmp.append(user)

    return tmp


def add_not_present_users(first_list, second_list):
    for user in first_list:
        if user not in second_list:
            second_list.append(user)


def analyse_results(spam_filter=False):
    global email_sent
    global email_opened
    global clicked_link
    global submitted_data
    global email_reported

    email_reported = remove_duplicate_users(email_reported)
    submitted_data = remove_duplicate_users(submitted_data)

    if spam_filter:
        tmp_1 = remove_spam_filter_noise(clicked_link)
        clicked_link = remove_duplicate_users(tmp_1)

        tmp_2 = remove_spam_filter_noise(email_opened)
        email_opened = remove_duplicate_users(tmp_2)
    else:
        clicked_link = remove_duplicate_users(clicked_link)
        email_opened = remove_duplicate_users(email_opened)

    email_sent = remove_duplicate_users(email_sent)

    add_not_present_users(submitted_data, clicked_link)
    add_not_present_users(clicked_link, email_opened)
    add_not_present_users(email_opened, email_sent)


def print_campaign_results():
    print(f"Email Sent: {len(email_sent)}")
    print(f"Email Opened: {len(email_opened)}")
    print(f"Clicked Link: {len(clicked_link)}")
    print(f"Submitted Data: {len(submitted_data)}")
    print(f"Email Reported: {len(email_reported)}")


def get_data_from_index(index, data_list):
    if len(data_list) - 1 < index:
        return ""
    else:
        return data_list[index]


def export_data_to_csv(output_file):
    global email_sent
    global email_opened
    global clicked_link
    global submitted_data
    global email_reported

    with open(output_file, "w") as csv_file:
        fieldnames = ["Email Sent", "Email Opened", "Clicked Link", "Submitted Data", "Email Reported"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for index in range(0, len(email_sent)):
            email_sent_col = email_sent[0]
            email_opened_col = get_data_from_index(index, email_opened)
            clicked_link_col = get_data_from_index(index, clicked_link)
            submitted_data_col = get_data_from_index(index, submitted_data)
            email_reported_col = get_data_from_index(index, email_reported)

            writer.writerow({"Email Sent": email_sent_col,
                             "Email Opened": email_opened_col,
                             "Clicked Link": clicked_link_col,
                             "Submitted Data": submitted_data_col,
                             "Email Reported": email_reported_col})


def main():
    args = parser.parse_args()

    get_data_from_file(args.file)
    
    analyse_results(args.filter)

    print_campaign_results()

    if args.output:
        export_data_to_csv(args.output)


if __name__ == "__main__":
    main()
