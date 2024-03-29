QUERIES = {
    # users
    'add_user': '''
        INSERT INTO User (id, name, nickname, company_id)
        VALUES ("{id}", "{name}", "{nickname}", "{company_id}");
        ''',

    'get_users': '''
        SELECT SQL_NO_CACHE id, name, nickname FROM User
        WHERE presence = true and company_id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        );
        ''',

    'update_user_presence': '''
        UPDATE User SET presence = {presence}
        WHERE id = "{id}";
        ''',

    'update_user_lunch_id': '''
        UPDATE User SET lunch_id = {lunch_id}
        WHERE id = "{id}";
        ''',

    'get_user': '''
        SELECT SQL_NO_CACHE * FROM User
        WHERE id = "{id}";
        ''',

    # lunch
    'get_lunches': '''
        SELECT SQL_NO_CACHE id, name, votes_count FROM Lunch
        WHERE company_id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        )
        ORDER BY votes_count DESC
        LIMIT 7;
        ''',

    'increase_lunch_votes_count': '''
        UPDATE Lunch SET votes_count = votes_count + 1
        WHERE id = {id};
        ''',

    'decrease_lunch_votes_count': '''
        UPDATE Lunch SET votes_count = votes_count - 1
        WHERE id = {id};
        ''',

    'add_lunch': '''
        INSERT INTO Lunch (name, company_id)
        VALUES ("{name}", "{company_id}");
        ''',

    'get_lunch': '''
        SELECT SQL_NO_CACHE * FROM Lunch WHERE id = {id};
    ''',

    'get_last_lunch': '''
        SELECT SQL_NO_CACHE id FROM Lunch ORDER BY id DESC LIMIT 1;
        ''',

    'delete_lunch': '''
        DELETE FROM Lunch WHERE id = {id};
    ''',

    # company
    'add_company': '''
        INSERT INTO Company (id, name)
        VALUES ("{id}", "{name}");
        ''',

    'get_company': '''
        SELECT SQL_NO_CACHE id, name, employees_count FROM Company
        WHERE id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        );
        ''',

    'get_companies': '''
        SELECT SQL_NO_CACHE id, name, employees_count FROM Company;
        ''',

    # reset_db
    'reset_user_lunch_id': '''
        UPDATE User SET lunch_id = NULL;
    ''',

    'reset_user_presence': '''
        UPDATE User SET presence = false;
    ''',

    'reset_lunch': '''
        DELETE FROM Lunch;
    '''
}
