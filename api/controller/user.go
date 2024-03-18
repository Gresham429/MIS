package controller

import (
	"MIS/auth"
	"MIS/model"
	"net/http"
	"strconv"
	"time"

	"github.com/labstack/echo/v4"
	"golang.org/x/crypto/bcrypt"
)

type registerRequest struct {
	UserName string `json:"username"`
	Password string `json:"password"`
}

// Register - 用户注册
func Register(c echo.Context) error {
	registerUser := new(registerRequest)
	if err := c.Bind(registerUser); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "请求的 JSON 格式错误"})
	}

	if registerUser.UserName == "" || registerUser.Password == "" {
		return c.JSON(http.StatusBadRequest, Response{Error: "用户名和密码不可以为空"})
	}

	// 检查用户是否已经存在
	existingUser, err := model.GetUserInfo(registerUser.UserName)
	if existingUser != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "用户名已存在"})
	}

	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 对密码进行哈希处理
	hashPassword, err := bcrypt.GenerateFromPassword([]byte(registerUser.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	registerUser.Password = string(hashPassword)

	user := &model.User{
		UserName: registerUser.UserName,
		Password: registerUser.Password,
		IsAdmin: true,
		IsSuperAdmin: true,
	}

	// 创建用户
	if err := model.CreateUser(user); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusCreated, Response{Message: "注册成功"})
}

type loginRequest struct {
	UserName string `json:"username"`
	Password string `json:"password"`
}

type loginResponse struct {
	Token string `json:"token"`
}

// Login - 用户登录(生成JWT令牌)
func Login(c echo.Context) error {
	loginUser := new(loginRequest)
	if err := c.Bind(loginUser); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "Invalid request"})
	}

	// 检索用户信息
	user, err := model.GetUserInfo(loginUser.UserName)
	if user == nil {
		return c.JSON(http.StatusUnauthorized, Response{Error: "用户名或密码错误"})
	}

	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 核对密码信息
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(loginUser.Password)); err != nil {
		return c.JSON(http.StatusUnauthorized, Response{Error: "用户名或密码错误"})
	}

	// 生成 jwt 令牌
	jwt, err := auth.GenerateJWTToken(user.UserName, user.IsAdmin || user.IsSuperAdmin)
	if err != nil {
		return c.JSON(http.StatusUnauthorized, Response{Error: err.Error()})
	}

	response := loginResponse{Token: jwt}

	return c.JSON(http.StatusOK, Response{Data: response})
}

type userInfoResponse struct {
	UserName string `json:"username,omitempty"`
	FullName string `json:"full_name,omitempty"`
	Email    string `json:"email,omitempty"`
	Address  string `json:"address,omitempty"`
	Admin    bool   `json:"admin"`
}

// GetUser - 获取用户信息（需要JWT身份验证）
func GetUserInfo(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	userInfo, err := model.GetUserInfo(username)

	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	response := userInfoResponse{
		UserName: userInfo.UserName,
		FullName: userInfo.FullName,
		Email:    userInfo.Email,
		Address:  userInfo.Address,
		Admin:    userInfo.IsAdmin || userInfo.IsSuperAdmin,
	}

	return c.JSON(http.StatusOK, Response{Data: response})
}

type updateRequest struct {
	UserName string `json:"username"`
	FullName string `json:"full_name"`
	Address  string `json:"address"`
}

// UpdateUserInfo - 更新用户信息（需要JWT身份验证）
func UpdateUserInfo(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	userInfo, err := model.GetUserInfo(username)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	// 从请求中获得需要更新的用户信息
	updatedInfo := new(updateRequest)
	if err := c.Bind(updatedInfo); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "请求的 JSON 格式错误"})
	}

	if updatedInfo.UserName != "" {
		userInfo.UserName = updatedInfo.UserName
	}

	if updatedInfo.FullName != "" {
		userInfo.FullName = updatedInfo.FullName
	}

	if updatedInfo.Address != "" {
		userInfo.Address = updatedInfo.Address
	}

	// Save the updated user information to the database
	if err := model.UpdateUser(userInfo); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法更新用户信息"})
	}

	return c.JSON(http.StatusOK, Response{Message: "成功更新用户信息"})
}

// DeleteUser - 删除用户（需要JWT身份验证）
func DeleteUser(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	err := model.DeleteUser(username)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: "删除用户失败"})
	}

	return c.JSON(http.StatusOK, Response{Message: "删除用户成功"})
}

// SendVerificationCode - 发送 6 位邮箱验证码
func SendVerificationCode(c echo.Context) error {
	ctx := c.Request().Context()
	email := c.QueryParam("email")
	username := c.QueryParam("username")

	if email == "" || username == "" {
		return c.JSON(http.StatusBadRequest, Response{Error: "param 参数缺失"})
	}

	// 检查发送频率
	lastSentTime, err := model.GetLastSentTime(email, ctx)
	if err == nil {
		lastSentTimeInt, _ := strconv.ParseInt(lastSentTime, 10, 64)
		if time.Now().Unix()-lastSentTimeInt < 60 {
			return c.JSON(http.StatusBadRequest, Response{Error: "验证码发送频率过高，请稍后重试。"})
		}
	}

	// 生成验证码
	verificationCode := auth.GenerateVerificationCode()

	// 在这里发送邮件，使用生成的验证码
	err = auth.SendEmail(email, verificationCode, username)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 存储验证码和有效期到 Redis
	model.StoreVerificationCode(email, verificationCode, ctx)

	return c.JSON(http.StatusOK, Response{Message: "验证码已发送，请查收。"})
}

type registerEmailRequest struct {
	Email      string `json:"email"`
	VerifyCode string `json:"verify_code"`
}

// RegisterEmail - 验证邮箱验证码
func RegisterEmail(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	// 获取请求上下文
	ctx := c.Request().Context()

	request := new(registerEmailRequest)
	if err := c.Bind(request); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "无效的请求数据。"})
	}

	// 检查邮箱是否被注册
	existingUser, err := model.GetUserByEmail(request.Email)
	if existingUser != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "邮箱已被注册"})
	}

	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 验证验证码
	err = auth.VerifyVerificationCode(request.VerifyCode, request.Email, ctx)
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: err.Error()})
	}

	// 更新用户信息
	updateUser, err := model.GetUserInfo(username)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	updateUser.Email = request.Email

	// Save the updated user information to the database
	if err := model.UpdateUser(updateUser); err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法注册用户邮箱"})
	}

	return c.JSON(http.StatusOK, Response{Message: "验证码验证成功。"})
}

type loginWithEmailRequest struct {
	Email      string `json:"email"`
	VerifyCode string `json:"verify_code"`
}

// LoginWithEmail - 邮箱验证登录
func LoginWithEmail(c echo.Context) error {
	ctx := c.Request().Context()

	request := new(loginWithEmailRequest)
	if err := c.Bind(request); err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "无效的请求数据。"})
	}

	// 查询邮箱是否被注册
	existingUser, err := model.GetUserByEmail(request.Email)
	if existingUser == nil {
		return c.JSON(http.StatusBadRequest, Response{Error: "邮箱未被注册"})
	}

	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	// 验证验证码
	err = auth.VerifyVerificationCode(request.VerifyCode, request.Email, ctx)
	if err != nil {
		return c.JSON(http.StatusBadRequest, Response{Error: err.Error()})
	}

	// 生成 jwt 令牌
	jwt, err := auth.GenerateJWTToken(existingUser.UserName, existingUser.IsAdmin || existingUser.IsSuperAdmin)
	if err != nil {
		return c.JSON(http.StatusUnauthorized, Response{Error: err.Error()})
	}

	response := loginResponse{Token: jwt}

	return c.JSON(http.StatusOK, Response{Data: response})
}

// 获取用户的喜欢列表
func GetUserLikes(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	posts, err := model.GetUserLikes(username)
	if err != nil {
		return c.JSON(http.StatusNoContent, Response{Message: "喜欢列表为空"})
	}

	return c.JSON(http.StatusOK, Response{Data: posts})
}

// 获取用户所发的帖子
func GetUserPosts(c echo.Context) error {
	// 获取用户名
	username, ok := c.Get("username").(string)

	if !ok {
		// 类型断言失败，处理错误
		return c.JSON(http.StatusInternalServerError, Response{Error: "无法将 user_name 转换为字符串"})
	}

	posts, err := model.GetUserPosts(username)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, Response{Error: err.Error()})
	}

	return c.JSON(http.StatusOK, Response{Data: posts})
}
