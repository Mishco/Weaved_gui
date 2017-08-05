## Weaved with GUI

Application with GUI developed in **Kivy** framework https://kivy.org/. This app create connection to server on local network. Created tunnel is ssh or www.

## Code Example

Using Kivy and weaved. Kivy is python framework. Weaved https://www.remot3.it/web/remot3-it-is-the-new-weaved.html is a service than create tunnel between device and your actual network.

```
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()
```


## Motivation

Motivation was VPN problem on local network and DNS free services.

## Installation

Provide code examples and explanations of how to get the project.

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests

Describe and show how to run the tests with code examples.

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

Free License

