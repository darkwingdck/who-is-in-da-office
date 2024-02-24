QUERIES = {
        # lunch
        'get_lunch_list': '''
        SELECT * FROM Lunch
        WHERE company_id = {company_id}
        SORTED BY votes_count DESC;
        ''',

        'update_user_lunch_id': '''
        UPDATE User SET lunch_id = {lunch_id}
        WHERE user_id = {user_id} and company_id = {company_id}
        ''',

        'update_lunch_votes_count': '''
        UPDATE Lunch SET votes_count = votes_count + 1
        WHERE lunch_id = {lunch_id} and company_id = {company_id};
        ''',

        'add_lunch': '''
        INSERT INTO Lunch (name, company_id)
        VALUES ({lunch_name}, {company_id});
        ''',

        # office
        'get_users': '''
        SELECT * FROM User
        WHERE company_id = {company_id} and present_tomorrow = true;
        ''',

        'update_user_presence': '''
        UPDATE User SET present_tomorrow = {present_tomorrow}
        WHERE id = {user_id};
        ''',
        
        # others
        'add_company': '''
        INSERT INTO Company (name, code)
        VALUES ({company_name}, {company_code});
        ''',

        'add_user': '''
        INSERT INTO User (name, chat_id, company_id)
        VALUES ({name}, {chat_id}, {company_id});
        ''',
        }
