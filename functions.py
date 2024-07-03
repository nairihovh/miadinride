def generateText(user_option, step, text=""):
    msg = ""
    if step == "choose_option":
        if text == "Գնում եմ, կտանեմ" or user_option.get("type") == "is_going":
            msg = "Ո՞ր քաղաքից եք շարժվելու:\nԳրեք քաղաքի կամ գյուղի անվանումը (օր. Վանաձոր)"
        elif text == "Ցանկանում եմ գնալ" or user_option.get("type") == "want_to_go":
            msg = "Ո՞ր քաղաքից եք ուզում գնալ:\nԳրեք քաղաքի կամ գյուղի անվանումը (օր. Վանաձոր)"

    if step == "is_going":
        msg = (f"Դուք շարժվում եք ***{user_option.get('from')}*** քաղաքից\n"
               f"Նշեք թե դեպի որ ուղղությամբ եք գնալու։ (օր. Երևան)")
    if step == "want_to_go":
        msg = (f"Դուք ցանկանում եք գնալ ***{user_option.get('from')}*** քաղաքից\n"
               f"Նշեք թե դեպի որ ուղղությամբ եք գնալու։ (օր. Երևան)")
    if step == "from":
        msg = (f"Դուք գնում եք ***{user_option.get('from')}-ից {user_option.get('to')}***\n"
               f"Նշեք թե երբ եք գնալու։")
    if step == "to":
        if user_option.get('type') == 'want_to_go':
            msg = (f"Դուք ***{user_option.get('when')}*** ցանկանում եք ***{user_option.get('from')}***-ից գնալ "
                   f"***{user_option.get('to')}***\n"
                   f"Նշեք թե քանի հոգով եք։ (օր. 1, 2, 5)")
        elif user_option.get('type') == "is_going":
            msg = (f"Դուք ***{user_option.get('when')} {user_option.get('from')}***-ից  գնում եք "
                   f"***{user_option.get('to')}***\n"
                   f"Նշեք թե քանի տեղ ունեք մեքենայի մեջ։ (օր. 5)")
    if step == "when":
        if user_option.get('type') == 'want_to_go':
            msg = (f"Դուք ***{user_option.get('count')}*** հոգով\n"
                   f"ցանկանում եք ***{user_option.get('when')} {user_option.get('from')}***-ից  գնալ "
                   f"***{user_option.get('to')}***\n"
                   f"Նշեք թե մեկ անձի համար որքան եք պատրաստ վճարել։\n(օր. 500, 1000, անվճար, 1000-2000)")
        elif user_option.get('type') == 'is_going':
            msg = (f"Մեքենայի մեջ կա ***{user_option.get('count')}*** տեղ\n"
                   f"Դուք ***{user_option.get('when')} {user_option.get('from')}***-ից  գնում եք "
                   f"***{user_option.get('to')}***\n"
                   f"Նշեք մեկ անձի համար պահանջվող գումարի չափը դրամով։\n(օր. 500, 1000, անվճար)")
    if step == 'count':
        if user_option['type'] == "want_to_go":
            msg = (f"Դուք ***{user_option.get('count')}*** հոգով\n"
                   f"ցանկանում եք ***{user_option.get('when')} {user_option.get('from')}***-ից  գնալ "
                   f"***{user_option.get('to')}***\n"
                   f"Մեկ անձի համար պատրաստ եք վճարել {user_option.get('price')} AMD ")
        else:
            msg = (f"Մեքենայի մեջ կա ***{user_option.get('count')}*** տեղ\n"
                   f"Դուք ***{user_option.get('when')} {user_option.get('from')}***-ից  գնում եք "
                   f"***{user_option.get('to')}***\n"
                   f"Մեկ անձի արժեքը՝ {user_option.get('price')} AMD")
    return msg