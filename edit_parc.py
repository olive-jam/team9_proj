# /blog/tests.py
# (... 생략 ...)
def test_comment_update(self):

    comment_by_trump = Comment.objects.create(
        post=self.post_001,
        author=self.user_trump,
        content='트럼프의 댓글입니다.'
    )
    # 로그인하지 않은 상태에서 댓글이 2개 있는 self.post_001 페이지를 연다.
    response = self.client.get(self.post_001.get_absolute_url())
    self.assertEqual(response.status_code, 200)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 댓글 영역에 수정 버튼이 둘 다 보이지 않아야 한다.
    # id는 comment-{pk}-update-btn으로 한다.
    comment_area = soup.find('div', id='comment-area')
    self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
    self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

    # obama로 로그인한 상태
    self.client.login(username='obama', password='somepassword')
    response = self.client.get(self.post_001.get_absolute_url())
    self.assertEqual(response.status_code, 200)
    soup = BeautifulSoup(response.content, 'html.parser')

    # obama로 로그인했으므로 trump가 작성한 댓글에 대한 수정 버튼은 보이지 않아야 한다.
    comment_area = soup.find('div', id='comment-area')
    self.assertFalse(comment_area.find('a', id='comment-2-update-btn')
    # 반면에 obama가 작성한 self.comment_001에 대한 수정 버튼은 나타나야 한다.)
    comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn'))
    # 이 수정버튼에는 'edit'이라고 써 있어야 한다.
    self.assertIn('edit', comment_001_update_btn.text)
    # 이 버튼에는 링크 경로를 담은 href 속성이 있어야 하는데, 이 경로는 'blog/update_comment/{pk}/'로 한다.
    self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')