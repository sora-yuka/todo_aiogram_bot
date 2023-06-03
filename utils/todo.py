class Get:
    def get_todo_list(self) -> str:
        with open("TODO.txt", "r") as file:
            result = file.read()
        return result


class Add:
    def add_point_to_list(self, todo_title,): # todo_description, todo_deadline):
        with open("TODO.txt", "r") as file:
            id = 0
            if file == None:        
                with open("TODO.txt", "w", encoding="utf-8") as file:
                    file.write(f"{id}. {todo_title}\n")#, todo_description, todo_deadline)
            
            with open("TODO.txt", "a+", encoding="utf-8") as file:
                file.write(f"{id}. {todo_title}\n")#, todo_description, todo_deadline)
            id += 1
            