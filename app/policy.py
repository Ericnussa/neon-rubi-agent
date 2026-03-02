class ActionPolicy:
    def require_confirmation(self, action_type: str) -> str:
        if action_type == "external_action":
            return "I can do that, but confirm first: this would perform an external/public action."
        return "Action blocked until confirmation."
