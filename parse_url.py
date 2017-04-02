
def parse_links(soup):
    blocks = soup.findAll("div", {"class": "md"})

    author = soup.find("p", {"class": "tagline"})

    try:
        author = author.find("a", {"class": "author"}).text
    except Exception as e:
        author = "None"
        pass

    try:
        date = soup.find("div", {"class": "date"})
        date = date.find("time").text
    except:
        date = "Unknown date"
        pass

    score = soup.find("div", {"class": "score"})

    try:
        score = score.find("span", {"class": "number"}).text
    except:
        score = 0
        pass

    i = 0
    post = []
    comments = []
    for block in blocks:
        if i == 0:
            i += 1
            continue
        if i == 1:
            i += 1
            lines = block.findAll('p')
            for line in lines:
                post.append(line.text)
            continue

        lines = block.findAll('p')
        for line in lines:
            comments.append(line.text)

    dict = {}
    dict['author'] = author
    dict['date'] = date
    dict['score'] = score
    dict['post'] = post
    dict['comments'] = comments

    # print(dict['comments'])
    # print(dict['post'])
    return dict

# parse_links("https://www.reddit.com/r/blackhat/comments/62810k/school_project_what_exploit_can_i_do_to_these/")
