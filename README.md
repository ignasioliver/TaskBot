# TaskBot - [HackUPC Winter 2017](https://hackupc2017w.devpost.com/)
>Chatbot developed at [HackUPC](https://hackupc.com/). Check it out at [DevPost](https://devpost.com/software/taskbot).

__Telegram task-manager-chatbot that keeps a list with your stuff.__

Just text what do you have to do and it will keep track of it in a gracefully way.

Its reaction and the way it talks depends on how you talk with him!

Test it! Chat with `@thetaskbot` on [Telegram](http://telegram.me/ubica_bot).

__The bot is not running 24/7. You can chat with it anytime, but it may not respond at the moment.__

More information -such as all the commands TaskBot knows- can be found at [taskbot.tech](http://taskbot.ignasioliver.com/).
## How is it done?
With Python and SQLite3. It was connected to an Everis API that processed natural language. Unfortunately, it is no longer available. However, `taskbot_adapted.py` does work without the language processing part.
## Usage examples
![screenshot1](http://ignasioliver.com/public/taskbot.png)
## Can I use it?
Yes. Follow the steps:

1. [Create a Telegram bot](https://core.telegram.org/bots). Give it the name you want. Have the token that BotFather gives you handy.

2. Import (or [fork](https://help.github.com/articles/fork-a-repo/)) this repo - following the [MIT License](LICENSE).

3. It is recommended to use `taskbot_adpated.py` instead of `taskbot.py` since the former doesn't include the Everis API connection, which at the time of writing is out of service. Hence `taskbot.py` can be deleted. On line `25` of `taskbot_adapted.py` change `insertTokenHere` to the token given by BotFather.

4. Run `taskbot.py` - or `taskbot_adapted` if you chose it . If you want to make it run independently from your computer you can deploy your project to services such as [Heroku](https://www.heroku.com/) or [DigitalOcean](https://www.digitalocean.com/).

5. Search on Telegram for the bot name you chose earlier. If it doesn't text anything, text `/start` and have fun!

Considering that the project was developed in a hackathon, the code is not well enough documented for production. If any question arises, I am available at `ignasi@ignasioliver.com`.
## Author
[Ignasi Oliver](http://www.ignasioliver.com/).
