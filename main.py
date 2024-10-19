import sql
from pandas import DataFrame
from random import choice

def main() -> None:
    print('----Bem-vindo a sua lista de afazeres!----\n------------------------------------------\n')
    def ask() -> str:
        print('O que gostaria de fazer agora?')
        print('a) Adicionar uma tarefa.')
        print('d) Deletar uma tarefa.')
        print('r) Realizar uma tarefa aleatória.')
        print('m) Marcar uma tarefa como finalizada.')
        print('v) Visualizar todas as tarefas.')
        print('e) Encerrar o programa.')
        return input('Sua resposta: ')
    
    answer: str = ask()
    while True:
        match answer.lower():
            case 'a':
                task: str = input('\nDigite a nova tarefa a ser adicionada: ')
                sql_comand: str = f"""
                    INSERT INTO todo_list (tarefa)
                    VALUES ('{task}');
                """
                sql.execute(sql_comand)
                print(f'Tafera adicionada com sucesso: {task}\n')
                answer: str = ask()
            case 'd':
                sql_comand: str = """
                    SELECT
                        id,
                        tarefa,
                        data_inicio
                    FROM todo_list
                    WHERE data_fim IS NULL;
                """
                df: DataFrame = sql.read(sql_comand)
                print(f'\n{df.to_string(index=False)}\n')
                id_chosen: int = int(input('Qual o id da tarefa a ser excluída? '))
                sql_comand: str = f"""
                    DELETE FROM todo_list
                    WHERE id = {id_chosen};
                """
                sql.execute(sql_comand)
                print(f'Tafera excluida com sucesso.\n')
                answer: str = ask()
            case 'r':
                sql_comand: str = """
                    SELECT
                        id,
                        tarefa,
                        data_inicio
                    FROM todo_list
                    WHERE data_fim IS NULL;
                """
                df: DataFrame = sql.read(sql_comand)
                id_chosen: list[int] = choice(df['id'])
                print('\nA tarefa selecionada foi: {0}\n'.format(df[df['id'].eq(id_chosen)]['tarefa'].values[0]))
                realizada: str = input('Tarefa realizada? (s/n) ')
                match realizada.lower():
                    case 's':
                        sql_comand: str = f"""
                            UPDATE todo_list
                            SET data_fim = CURRENT_DATE
                            WHERE id = {id_chosen};
                        """
                        sql.execute(sql_comand)
                        answer: str = ask()
                    case _:
                        answer: str = ask()
            case 'm':
                sql_comand: str = """
                    SELECT
                        id,
                        tarefa,
                        data_inicio
                    FROM todo_list
                    WHERE data_fim IS NULL;
                """
                df: DataFrame = sql.read(sql_comand)
                print(f'\n{df.to_string(index=False)}\n')
                id_chosen: int = int(input('Qual o id da tarefa finalizada? '))
                sql_comand: str = f"""
                    UPDATE todo_list
                    SET data_fim = CURRENT_DATE
                    WHERE id = {id_chosen};
                """
                sql.execute(sql_comand)
                print(f'Tafera marcada como finalizada com sucesso.\n')
                answer: str = ask()
            case 'v':
                sql_comand: str = """
                    SELECT
                        CASE WHEN data_fim IS NULL THEN 'Não realizada' ELSE 'Realizada' END AS status,
                        tarefa,
                        data_inicio,
                        data_fim
                    FROM todo_list;
                """
                df: DataFrame = sql.read(sql_comand)
                print(f'\n{df}\n')
                answer: str = ask()
            case 'e':
                break
            case _:
                print('\nPor favor, envie uma resposta apropriada.\n')
                answer: str = ask()

if '__main__' == __name__:
    main()