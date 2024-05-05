module default {

    abstract type DatedType {
        created: datetime {
            rewrite insert using (datetime_of_statement())
        }
        modified: datetime {
            rewrite insert using (datetime_of_statement());
            rewrite update using (datetime_of_statement());
        }
    }


    type Protagonist extending DatedType {
        name: str {
            constraint exclusive;
        }
        gender: str;
        nicknames: array<str>;
        age: int64;
        occupation: array<str>;
        nationality: array<str>;
        physical_characteristics: array<str>;
        profile_description: str;
    }
}