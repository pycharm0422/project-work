def check_message_intention(message):
    abusive_word_list = ["Cumbubble",
    "Fuck",
    "Shitbag",
    "Shit",
    "Piss off",
    "Asshole",
    "Dickweed",
    "Cunt",
    "bitch",
    "Bastard",
    "Bitch",
    "Damn",
    "Bollocks",
    "Bugger",
    "Cocknose",
    "Bloody hell",
    "Knobhead",
    "Choad",
    "Bitchtits",
    "Crikey",
    "Rubbish",
    "Pissflaps",
    "Shag",
    "Wanker",
    "Talking the piss",
    "Twat",
    "Arsebadger",
    "Jizzcock",
    "Cumdumpster",
    "Shitmagnet",
    "Scrote",
    "Twatwaffle",
    "Thundercunt",
    "Dickhead",
    "Shitpouch",
    "Jizzstain",
    "Nonce",
    "Pisskidney",
    "Wazzock",
    "Cumwipe",
    "Fanny",
    "Bellend",
    "Pisswizard",
    "Knobjockey",
    "Cuntpuddle",
    "Dickweasel",
    "Quim",
    "Bawbag",
    "Fuckwit",
    "Tosspot",
    "Cockwomble",
    "Twat face",
    "Cack",
    "Flange",
    "Clunge",
    "Dickfucker",
    "Fannyflaps",
    "Wankface",
    "Shithouse",
    "Gobshite",
    "Jizzbreath",
    "Todger",
    "Nutsack"]


    hate_word_lst = [
        'terrorist',
        'dead',
        'die',
        'kill',
        'murder',
        'rape',
        'horny',
        ''
    ]

    abuse_lst = []


    deny = ['no', 'not', 'none', 'eliminated', 'dont']


    lst_of_sentences = [
        'girls should not go to school',
        'women are not great as man',
        'women should work under man',
        '',
        '',
        '',
    ]

    for j in abusive_word_list:
        abuse_lst.append(j.lower())

    
    a_lst = message.split(" ")
    hate_flag = False
    abuse_flag = False
    for i in a_lst:
        if i.lower() in abuse_lst:
            abuse_flag = True

    for i in a_lst:
        if i.lower() in hate_word_lst:
            hate_flag = True


    for i in a_lst:
        if i.lower() in deny:
            hate_flag = False

    for i in lst_of_sentences:
        if i == message:
            hate_flag = True
    if hate_flag:
        return "hate_speech"
    elif abuse_flag:
        return "abusive_speech"
    else:
        return "fine_speech"
