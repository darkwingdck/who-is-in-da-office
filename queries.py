QUERIES = {
    # users
    'add_user': '''
        INSERT INTO User (id, name, company_id)
        VALUES ("{id}", "{name}", "{company_id}");
        ''',

    'get_users': '''
        SELECT id, name FROM User
        WHERE presence = true and company_id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        );
        ''',

    'update_user_presence': '''
        UPDATE User SET presence = {presence}
        WHERE id = "{id}";
        ''',

    'get_user': '''
        SELECT * FROM User
        WHERE id = "{id}";
        ''',

    'get_company_name_by_id': '''
        SELECT name from Company
        WHERE id = "{id}";
        ''',
    # lunch
    'get_lunch_list': '''
        SELECT * FROM Lunch
        WHERE company_id = (
            SELECT company_id FROM User
            WHERE chat_id = "{chat_id}"
        )
        ORDER BY votes_count DESC;
        ''',

    'update_user_lunch_id': '''
        UPDATE User SET lunch_id = {lunch_id}
        WHERE chat_id = "{chat_id}";
        ''',

    'update_lunch_votes_count': '''
        UPDATE Lunch SET votes_count = votes_count + 1
        WHERE lunch_id = {lunch_id} and company_id = (
            SELECT company_id FROM User
            WHERE chat_id = "{chat_id}"
        );
        ''',

    'add_lunch': '''
        INSERT INTO Lunch (name, company_id)
        VALUES ("{lunch_name}", {company_id});
        ''',

    # office


    # others
    'add_company': '''
        INSERT INTO Company (name, code)
        VALUES ("{company_name}", "{company_code}");
        ''',


    'get_companies': '''
        SELECT * FROM Company;
        ''',
}
