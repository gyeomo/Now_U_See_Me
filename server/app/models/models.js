const config = require('../config/environment');
const Sequelize = require('sequelize');

const sequelize = new Sequelize(
    config.mysql.database,
    config.mysql.username,
    config.mysql.password, {
        host: 'localhost',
        dialect: 'mysql'
    }
);

const User = sequelize.define('user', {
    name: Sequelize.STRING,
    token: Sequelize.STRING
});

const Event = sequelize.define('event', {
    eventTime: Sequelize.STRING,
    // sequelize.string default 255
    //types- 0: fresh, 1: unknown, 2: family, 3: friends
    types: Sequelize.STRING,
    img_addrs: Sequelize.STRING
    // {
    //     type: Sequelize.STRING,
    //     validate: {
    //         len: [0, 1500]
    //     }
    // }

});


module.exports = {
    sequelize: sequelize,
    User: User,
    Event: Event
}