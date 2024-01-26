import streamlit as st
import os
import shutil


blog_directory = 'blog'
os.makedirs(blog_directory, exist_ok=True)

def admin_upload():
    st.title('Admin Upload Page')

    article_title = st.text_input('Article Title')
    article_content = st.text_area('Article Content')


    uploaded_image = st.file_uploader('Upload an Image', type=['jpg', 'png', 'jpeg'])
    if st.button('Upload Article'):
        filename = os.path.join(blog_directory, f'{article_title}.md')
        # Save the article content to a file
        with open(filename, 'w') as f:
            f.write(article_content)

        # Save the uploaded image to the blog directory
        if uploaded_image is not None:
            image_filename = os.path.join(blog_directory, f'{article_title}.png')
            with open(image_filename, 'wb') as img_file:
                img_file.write(uploaded_image.read())

        st.success('Article uploaded successfully!')
        
    # Function to delete a file
    def delete_file(filename):
        if os.path.exists(filename):
            os.remove(filename)
            st.success(f"Deleted file: {filename}")
        else:
            st.error("The file does not exist")

    st.title("Delete Uploaded Files")
    for file in os.listdir(blog_directory):
        if file.endswith('.md') or file.endswith('.png'):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(file)
            with col2:
                if st.button("Delete", key=file):
                    delete_file(os.path.join(blog_directory, file))

def add_admin_reply(post_title, reply):
    comment_file = os.path.join(blog_directory, f'{post_title}_comments.txt')
    with open(comment_file, 'a') as file:
        file.write(f"{reply} (admin)\n")

def display_comments_and_reply(post_title):
    st.subheader('Comments')
    comment_file = os.path.join(blog_directory, f'{post_title}_comments.txt')
    if os.path.exists(comment_file):
        with open(comment_file, 'r') as file:
            for comment in file:
                if "(user)" in comment:
                    st.text(comment.strip())
                    reply = st.text_input('Reply:', key=f'reply_{comment}')
                    if st.button('Post Reply', key=f'post_reply_{comment}'):
                        add_admin_reply(post_title, reply)
                        st.success('Reply posted! (admin)')
                else:
                    st.text(comment.strip())


def admin_view():
    st.title('Admin View')

    # List all the available articles in the blog directory
    articles = [f for f in os.listdir(blog_directory) if f.endswith('.md')]

    # Display articles, comments, and allow admin to reply
    for article in articles:
        article_title = article.split('.')[0]
        st.subheader(article_title)
        with open(os.path.join(blog_directory, article), 'r') as f:
            st.write(f.read())

        # Display associated images, if available
        image_filename = os.path.join(blog_directory, f'{article_title}.png')
        if os.path.exists(image_filename):
            st.image(image_filename, caption=f'Image for {article_title}')
        display_comments_and_reply(article_title)
        st.markdown('---')
   


    
# Main App
def main():
    st.sidebar.title('Blog App')
    
    if st.sidebar.button('Logout'):
        st.session_state.clear()
        st.empty()  
        st.success("You have been logged out.")
        st.info("To log in again, please manually open the `login.py` script.")
        st.markdown("Navigate to the script's location and run it. For example:")
        st.code("streamlit run C:\\Users\\User\\Desktop\\final project\\Codes\\login.py")
        return
    
    
    page = st.sidebar.selectbox('Select Page', ['Admin Upload', 'User View'])

    if page == 'Admin Upload':
        admin_upload()
    elif page == 'User View':
        admin_view()
        

if __name__ == '__main__':
        main()
