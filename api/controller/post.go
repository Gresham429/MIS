package controller

import (
	"MIS/model"
	"net/http"
	"strconv"

	"github.com/labstack/echo/v4"
)

type createPostRequest struct {
	Content        string   `json:"content"`
	NodeID         uint     `json:"node_id"`
	MentionedUsernames []string `json:"mentioned_usernames"`
}

// PublishPost - 发布帖子
func PublishPost(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	// 获取请求信息
	req := new(createPostRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "请求的 JSON 格式错误"})
	}

	// 创建帖子
	postID, err := model.CreatePost(req.Content, username, req.NodeID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	for _, mentionedUsername := range req.MentionedUsernames {
		user, _ := model.GetUserInfo(mentionedUsername)
		if user == nil {
			model.DeletePost(postID)
			return c.JSON(http.StatusBadRequest, Response{Error: "提到的用户不存在"})
		}

		model.CreateMentionInPost(postID, mentionedUsername)
	}

	return c.JSON(http.StatusCreated, Response{Message: "发布成功"})
}

type deletePostRequest struct {
	PostID uint `json:"post_id"`
}

// DeletePost - 删除帖子
func DeletePost(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)
	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	// 获取是否为管理员
	IsAdmin, ok := c.Get("admin").(bool)
	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 admin 转换为布尔值"})
	}

	// 获取请求信息
	req := new(deletePostRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "请求的 JSON 格式错误"})
	}

	// 获取帖子信息
	post, err := model.GetPostInfo(req.PostID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 检查用户是否有权限删除帖子
	if post.Author != username && !IsAdmin {
		return c.JSON(http.StatusForbidden, Response{Error: "无权限删除帖子"})
	}

	// 删除提到的用户
	if err := model.DeleteMentionInPost(req.PostID); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 删除帖子
	if err := model.DeletePost(req.PostID); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 删除帖子下的评论
	if err := model.DeleteCommentsInPost(req.PostID); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 删除帖子下的点赞
	if err := model.DeleteLikesInPost(req.PostID); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Message: "删除帖子成功"})
}

// GetPost - 获取帖子信息
func GetPostInfo(c echo.Context) error {
	// 获取请求信息
	postID, err := strconv.Atoi(c.Param("post_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "Post ID 不合法"})
	}

	// 获取帖子信息
	post, err := model.GetPostInfo(uint(postID))
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Data: post})
}

type createCommentRequest struct {
	Content string `json:"content"`
}

// PublishComment - 发布评论
func PublishComment(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}


	// 获取 postID
	postID, err := strconv.Atoi(c.Param("post_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "Invalid post ID"})
	}

	// 获取请求信息
	req := new(createCommentRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "请求的 JSON 格式错误"})
	}

	// 创建评论
	err = model.CreateComment(uint(postID), username, req.Content)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 获取帖子信息
	post, err := model.GetPostInfo(uint(postID))
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 更新评论数量
	post.CommentsNum++
	if err := model.UpdatePost(post); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusCreated, Response{Message: "发布评论成功"})
}

// 按照回复数分页返回某个节点的帖子列表
func GetPostListByCommentsNum(c echo.Context) error {
	// 获取请求信息
	nodeID, err := strconv.Atoi(c.Param("node_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "node ID 不合法"})
	}

	// 获取页码
	page, err := strconv.Atoi(c.QueryParam("page"))
	if err != nil {
		page = 1
	}

	// 获取每页的帖子数量
	pageSize, err := strconv.Atoi(c.QueryParam("page_size"))
	if err != nil {
		pageSize = 10
	}

	// 获取帖子列表
	posts, err := model.GetPostsByCommentsNum(uint(nodeID), page, pageSize)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Data: posts})
}

// 按照时间分页返回某个节点的帖子列表
func GetPostListByTime(c echo.Context) error {
	// 获取请求信息
	nodeID, err := strconv.Atoi(c.Param("node_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "node ID 不合法"})
	}

	// 获取页码
	page, err := strconv.Atoi(c.QueryParam("page"))
	if err != nil {
		page = 1
	}

	// 获取每页的帖子数量
	pageSize, err := strconv.Atoi(c.QueryParam("page_size"))
	if err != nil {
		pageSize = 10
	}

	// 获取帖子列表
	posts, err := model.GetPostsByTime(uint(nodeID), page, pageSize)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Data: posts})
}

type deleteCommentRequest struct {
	CommentID uint `json:"comment_id"`
}

// DeleteComment - 删除评论
func DeleteComment(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}


	// 获取请求信息
	req := new(deleteCommentRequest)
	if err := c.Bind(req); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "请求的 JSON 格式错误"})
	}

	// 获取评论信息
	comment, err := model.GetCommentInfo(req.CommentID)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 检查用户是否有权限删除评论
	if comment.Username != username {
		return c.JSON(http.StatusForbidden, Response{Error: "无权限删除评论"})
	}

	// 删除评论
	if err := model.DeleteComment(req.CommentID); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Message: "删除评论成功"})
}

// GetCommentList - 获取帖子下的评论列表
func GetCommentList(c echo.Context) error {
	// 获取 postID
	postID, err := strconv.Atoi(c.Param("post_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "Invalid post ID"})
	}

	// 获取评论列表
	comments, err := model.GetComments(uint(postID))
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Data: comments})
}

// LikePost - 点赞
func LikePost(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	// 获取 postID
	postID, err := strconv.Atoi(c.Param("post_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "Invalid post ID"})
	}

	// 点赞
	err = model.CreateLike(uint(postID), username)

	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 帖子点赞数加1
	post, err := model.GetPostInfo(uint(postID))
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	post.LikesNum++
	if err := model.UpdatePost(post); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Message: "点赞成功", Data: post.LikesNum})
}

// UnlikePost - 取消点赞
func RemovelikePost(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	// 获取 postID
	postID, err := strconv.Atoi(c.Param("post_id"))
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "Invalid post ID"})
	}

	// 取消点赞
	err = model.DeleteLike(uint(postID), username)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 帖子点赞数减1
	post, err := model.GetPostInfo(uint(postID))
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	post.LikesNum--
	if err := model.UpdatePost(post); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Message: "取消点赞成功", Data: post.LikesNum})
}

