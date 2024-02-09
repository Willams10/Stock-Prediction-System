import streamlit as st
import os

blog_directory = 'blog'

def add_user_comment(post_title, comment):
    comment_file = os.path.join(blog_directory, f'{post_title}_comments.txt')
    with open(comment_file, 'a') as file:
        file.write(f"{comment} (user)\n")


def display_comments(post_title):
    st.subheader('Comments')
    comment_file = os.path.join(blog_directory, f'{post_title}_comments.txt')

    # Display existing comments
    if os.path.exists(comment_file):
        with open(comment_file, 'r') as file:
            for comment in file:
                st.text(comment.strip())

    # Adding new user comments
    new_comment = st.text_input('Write a comment', key=f'new_comment_{post_title}')
    if st.button('Post Comment', key=f'post_comment_{post_title}'):
        add_user_comment(post_title, new_comment)
        st.success('Comment added! (user)')

# User View Page
def user_view():
    st.title('Blog')

    # List all the available articles in the blog directory
    articles = [f for f in os.listdir(blog_directory) if f.endswith('.md')]

    # Display articles and their comments
    for article in articles:
        st.subheader(article.split('.')[0])
        with open(os.path.join(blog_directory, article), 'r') as f:
            st.write(f.read())

        # Display associated images, if available
        image_filename = os.path.join(blog_directory, f'{article.split(".")[0]}.png')
        if os.path.exists(image_filename):
            st.image(image_filename, caption=f'Image for {article.split(".")[0]}')

        # Display and add comments
        display_comments(article.split('.')[0])
        st.markdown('---')

# Main function for the user app
def main():
    user_view()

if __name__ == '__main__':
    main()