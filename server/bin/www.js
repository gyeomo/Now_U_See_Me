const app = require('../app/app');
const port = 3000;
const hostname = '192.168.0.39';//'localhost';//'192.168.0.130';
const syncDatabase = require('./sync-database');

app.listen(port, hostname, () => {
    console.log('now_u_see_me app litensing on port 3000');

    syncDatabase().then(() => {
        console.log("Database sync");
    });
});