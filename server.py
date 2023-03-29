import streamlit as st
import numpy as np
import random
# First some code.
streamlit = "cool"
theming = "fantastic"
both = "💥"
primaryColor="green"
backgroundColor="#0E1117"
secondaryBackgroundColor="#262730"
textColor="#FAFAFA"
font="sans serif"



def init(post_init=False):
    if not post_init:
        st.session_state.opponent = 'Person'
        st.session_state.win = {'🍕': 0, '🥑': 0}
    st.session_state.board = np.full((3, 3), '.', dtype=str)
    st.session_state.player = '🍕'
    st.session_state.warning = False
    st.session_state.winner = None
    st.session_state.over = False



def check_available_moves(extra=False) -> list:
    raw_moves = [row for col in st.session_state.board.tolist() for row in col]
    num_moves = [i for i, spot in enumerate(raw_moves) if spot == '.']
    if extra:
        return [(i // 3, i % 3) for i in num_moves]
    return num_moves


def check_rows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return None


def check_diagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
        return board[0][len(board) - 1]
    return None


def check_state():
    if st.session_state.winner:
        st.success(f"Congratulations! {st.session_state.winner} you are the winner! 🤩")
    if st.session_state.warning and not st.session_state.over:
        st.warning('⚠️ Oops this move has already been taken')
    if st.session_state.winner and not st.session_state.over:
        st.session_state.over = True
        st.session_state.win[st.session_state.winner] = (
            st.session_state.win.get(st.session_state.winner, 0) + 1
        )
    elif not check_available_moves() and not st.session_state.winner:
        st.info(f'Not bad.. Its a TIE....💣')
        st.session_state.over = True


def check_win(board):
    for new_board in [board, np.transpose(board)]:
        result = check_rows(new_board)
        if result:
            return result
    return check_diagonals(board)


def computer_player():
    moves = check_available_moves(extra=True)
    if moves:
        i, j = random.choice(moves)
        handle_click(i, j)


def handle_click(i, j):
    if (i, j) not in check_available_moves(extra=True):
        st.session_state.warning = True
    elif not st.session_state.winner:
        st.session_state.warning = False
        st.session_state.board[i, j] = st.session_state.player
        st.session_state.player = "🥑" if st.session_state.player == "🍕" else "🍕"
        winner = check_win(st.session_state.board)
        if winner != ".":
            st.session_state.winner = winner


def main():
    st.write(
        """
        # Lets Play Tic Tac Toe........🍕 VS 🥑
        """
    )
    st.image('a.jpg', width=650)

    if "board" not in st.session_state:
        init()
    new_title = '<p style="font-family:sans-serif; color:black; font-size: 28px;">Configuration ⚙️-:</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    reset, score, player = st.columns(3)
    reset.button('Re-try it again!!', on_click=init, args=(True,))


    st.selectbox(
            'Select your opponet 💪',
            ['Person', 'Machine'],
            key='opponent',
            on_change=init,
            args=(True,),
        )

# Store the initial value of widgets in session state
    new_title1 = '<p style="font-family:sans-serif; color:black; font-size: 28px;">Tic Tac Toe Begin 🤼-:</p>'
    st.markdown(new_title1, unsafe_allow_html=True)


    
    for i, row in enumerate(st.session_state.board):
        cols = st.columns(5,gap='medium')
        for j, field in enumerate(row):
            cols[j + 1].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click
                if st.session_state.player == '🍕'
                or st.session_state.opponent == 'Person'
                else computer_player(),
                args=(i, j),
            )

    check_state()

    score.button(f'🍕{st.session_state.win["🍕"]} 🆚 {st.session_state.win["🥑"]}🥑')
    player.button(
        f'{"🍕" if st.session_state.player == "🍕" else "🥑"}\'s turn'
        if not st.session_state.winner
        else f'Game is Over. See you soon 😀'
    )
    
if __name__ == '__main__':
    main()
