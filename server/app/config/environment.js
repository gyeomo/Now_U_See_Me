const environment = {
    development: {
        mysql: {
            username: 'root',
            password: 'beyondme',
            database: 'now_u_see_me'
        },

        sequelize: {
            force: false
        }
    },

    test: {
        mysql: {
            username: 'root',
            password: 'beyondme',
            database: 'now_u_see_me_test'
        },
        
        sequelize: {
            force: true
        }
    },

    production: {

    }
}

const nodeEnv = process.env.NODE_ENV || 'development';

module.exports = environment[nodeEnv];