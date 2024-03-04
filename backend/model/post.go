package model

import (
	"time"
	"errors"
)

// Post - 帖子
type Post struct {
	PostID      uint      `gorm:"primaryKey;column:post_id"`
	Content     string    `gorm:"column:content"`
	Author      string    `gorm:"column:author"`
	NodeID      uint      `gorm:"column:node_id"`
	CreateTime  time.Time `gorm:"column:create_time"`
	LikesNum    uint      `gorm:"column:likes"`
	CommentsNum uint      `gorm:"column:comments_num"`
}

// 获取当前时间并返回格式化后的字符串
func getCurrentTime() time.Time {
	currentTime := time.Now()
	return currentTime
}

// 创建一个帖子
func CreatePost(content string, author string, nodeID uint) (uint, error) {
	newPost := Post{
		Content:     content,
		Author:      author,
		NodeID:      nodeID,
		CreateTime:  getCurrentTime(),
		LikesNum:    0,
		CommentsNum: 0,
	}

	// 将新帖子添加到数据库
	result := DB.Create(&newPost)
	if result.Error != nil {
		return 0, result.Error
	}

	// 返回新帖子的 postID
	return newPost.PostID, nil
}

// 读取帖子信息
func GetPostInfo(postID uint) (*Post, error) {
	post := &Post{}
	result := DB.Where("post_id = ?", postID).First(post)
	if result.Error != nil {
		return nil, result.Error
	}

	return post, nil
}

// 更新帖子信息
func UpdatePost(post *Post) error {
	result := DB.Save(post)
	return result.Error
}

// 删除帖子
func DeletePost(postID uint) error {
	result := DB.Where("post_id = ?", postID).Delete(&Post{})
	return result.Error
}

// 获取用户的帖子列表
func GetUserPosts(username string) ([]Post, error) {
	var posts []Post
	result := DB.Where("author = ?", username).Find(&posts)
	if result.Error != nil {
		return nil, result.Error
	}

	return posts, nil
}

// 按照回复数量排序读取摸个节点下的帖子列表，并作分页处理
func GetPostsByCommentsNum(nodeID uint, page int, pageSize int) ([]Post, error) {
	var posts []Post
	result := DB.Where("node_id = ?", nodeID).Order("comments_num desc").Offset((page - 1) * pageSize).Limit(pageSize).Find(&posts)

	if result.Error != nil {
		return nil, result.Error
	}

	return posts, nil
}

// 按照时间排序读取摸个节点下的帖子列表，并作分页处理
func GetPostsByTime(nodeID uint, page int, pageSize int) ([]Post, error) {
	var posts []Post
	result := DB.Where("node_id = ?", nodeID).Order("create_time desc").Offset((page - 1) * pageSize).Limit(pageSize).Find(&posts)

	if result.Error != nil {
		return nil, result.Error
	}

	return posts, nil
}

// MentionInPosts - 提到的用户
type MentionInPost struct {
	MentionInPostID uint   `gorm:"primaryKey;column:MentionInPost_id"`
	PostID          uint   `gorm:"column:post_id"`
	Username        string `gorm:"column:username"`
}

// 创建提到的用户
func CreateMentionInPost(postID uint, username string) error {
	newMentionInPost := MentionInPost{
		PostID:   postID,
		Username: username,
	}

	// 将提到的用户添加到数据库
	result := DB.Create(&newMentionInPost)
	if result.Error != nil {
		return result.Error
	}

	return nil
}

// 删除提到的用户
func DeleteMentionInPost(postID uint) error {
	result := DB.Where("post_id = ?", postID).Delete(&MentionInPost{})
	return result.Error
}

// 读取提到的用户
func GetMentionInPostedUsers(postID uint) ([]string, error) {
	var MentionInPosts []MentionInPost
	result := DB.Where("post_id = ?", postID).Find(&MentionInPosts)
	if result.Error != nil {
		return nil, result.Error
	}

	var usernames []string
	for _, MentionInPost := range MentionInPosts {
		usernames = append(usernames, MentionInPost.Username)
	}

	return usernames, nil
}

// Comments - 评论
type Comment struct {
	CommentID  uint      `gorm:"primaryKey;column:comment_id"`
	PostID     uint      `gorm:"column:post_id"`
	Username   string    `gorm:"column:username"`
	Content    string    `gorm:"column:content"`
	CreateTime time.Time `gorm:"column:create_time"`
}

// 创建评论
func CreateComment(postID uint, username string, content string) error {
	newComment := Comment{
		PostID:     postID,
		Username:   username,
		Content:    content,
		CreateTime: getCurrentTime(),
	}

	// 将评论添加到数据库
	result := DB.Create(&newComment)
	if result.Error != nil {
		return result.Error
	}

	return nil
}

// 读取评论信息
func GetCommentInfo(commentID uint) (*Comment, error) {
	comment := &Comment{}
	result := DB.Where("comment_id = ?", commentID).First(comment)
	if result.Error != nil {
		return nil, result.Error
	}

	return comment, nil
}

// 删除评论
func DeleteComment(commentID uint) error {
	result := DB.Where("comment_id = ?", commentID).Delete(&Comment{})
	return result.Error
}

// 读取帖子的评论列表
func GetComments(postID uint) ([]Comment, error) {
	var comments []Comment
	result := DB.Where("post_id = ?", postID).Find(&comments)
	if result.Error != nil {
		return nil, result.Error
	}

	return comments, nil
}

// 删除帖子下所有的评论
func DeleteCommentsInPost(postID uint) error {
	result := DB.Where("post_id = ?", postID).Delete(&Comment{})
	return result.Error
}

// 用户点赞表（每个用户对每个帖子只能点赞一次）
type Like struct {
	LikeID   uint   `gorm:"primaryKey;column:like_id"`
	PostID   uint   `gorm:"column:post_id"`
	Username string `gorm:"column:username"`
}

// 点赞
func CreateLike(postID uint, username string) error {
	// 检查用户是否已经点赞
	var like Like

	result := DB.Where("post_id = ? AND username = ?", postID, username).First(&like)
	if result.Error == nil {
		// 用户已经点赞
		return errors.New("用户已经点赞")
	}

	newLike := Like{
		PostID:   postID,
		Username: username,
	}

	// 将点赞信息添加到数据库
	result = DB.Create(&newLike)
	if result.Error != nil {
		return result.Error
	}

	return nil
}

// 取消点赞
func DeleteLike(postID uint, username string) error {
	result := DB.Where("post_id = ? AND username = ?", postID, username).Delete(&Like{})
	
	if result.Error != nil {
		return errors.New("取消点赞失败")
	}

	return nil
}

// 删除帖子的所有点赞
func DeleteLikesInPost(postID uint) error {
	result := DB.Where("post_id = ?", postID).Delete(&Like{})
	return result.Error
}

// 获得用户的喜欢列表
func GetUserLikes(username string) ([]Post, error) {
	var likes []Like
	result := DB.Where("username = ?", username).Find(&likes)
	if result.Error != nil {
		return nil, result.Error
	}

	var posts []Post
	for _, like := range likes {
		post, err := GetPostInfo(like.PostID)
		if err != nil {
			return posts, err
		}

		posts = append(posts, *post)
	}

	return posts, nil
}
