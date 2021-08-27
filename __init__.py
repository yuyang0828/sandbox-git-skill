from mycroft import MycroftSkill, intent_file_handler


class SandboxGit(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('git.sandbox.intent')
    def handle_git_sandbox(self, message):
        self.speak_dialog('git.sandbox')


def create_skill():
    return SandboxGit()

