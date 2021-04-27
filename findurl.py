def finder_url(link):
    st = link.find("url")
    fst = st + 4
    st = st+3
    active = True
    while active:
        if link[st] == "&":
            active = False
            continue
        st += 1
    complete = link[fst:st]
    return(complete)