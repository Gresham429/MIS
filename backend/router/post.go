package router

import (
	"MIS/controller"

	"github.com/labstack/echo/v4"
)

func InitPost(g *echo.Group) {
	g.POST("/publish_post", controller.PublishPost)
	g.DELETE("/delete_post", controller.DeletePost)
	g.GET("/get_post_info/:post_id", controller.GetPostInfo)
	g.POST("/publish_comment", controller.PublishComment)
	g.DELETE("/delete_comment", controller.DeleteComment)
	g.GET("/get_comment_list/:post_id", controller.GetCommentList)
	g.GET("/get_posts_by_comments_num/:node_id", controller.GetPostListByCommentsNum)
	g.GET("/get_posts_by_time/:node_id", controller.GetPostListByTime)
	g.GET("like_post/:post_id", controller.LikePost)
	g.GET("remove_like_post/:post_id", controller.RemovelikePost)
}