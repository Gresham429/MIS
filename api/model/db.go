package model

import (
	"context"
	"MIS/config"
	logger "MIS/log"
	"time"

	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB = nil
var RDB *redis.Client = nil

// 初始化 postgres
func initPostgres() error {
	dbConfig := config.JsonConfiguration.DB
	dsn := "host=" + dbConfig.Host + " user=" + dbConfig.User + " password=" + dbConfig.Password + " dbname=" + dbConfig.DBName + " port=" + dbConfig.Port + " sslmode=disable TimeZone=Asia/Shanghai"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})

	if err != nil {
		return err
	}

	// 自动迁移模型
	db.AutoMigrate(&User{}, &Post{}, &Node{})

	DB = db

	return nil
}

// 初始化 redis
func initRedis() error {
	redisConfig := config.JsonConfiguration.RDB

	rdb := redis.NewClient(&redis.Options{
		Addr:     redisConfig.Addr,
		Password: redisConfig.Password, // no password set
		DB:       redisConfig.DBIndex,  // use default DB
	})

	ctx := context.Background()

	_, err := rdb.Ping(ctx).Result()
	if err != nil {
		return err
	}

	RDB = rdb

	return nil
}

// 连接 postgres 与 redis
func ConnectDatabase() {
	var err error

	for DB == nil {
		err = initPostgres()
		if err != nil {
			logger.Logger.Error("Error connecting to the postgres: ", err)
			logger.Logger.Warn("Retrying in 5 seconds...")
			time.Sleep(5 * time.Second)
		}
	}

	logger.Logger.Info("Connect postgres successfully!")

	for RDB == nil {
		err = initRedis()
		if err != nil {
			logger.Logger.Error("Error connecting to the redis: ", err)
			logger.Logger.Warn("Retrying in 5 seconds...")
			time.Sleep(5 * time.Second)
		}
	}

	logger.Logger.Info("Connect redis successfully!")
}

// 关闭 postgres 与 redis
func CloseDatabase() {
	if DB != nil {
		db, err := DB.DB()
		if err != nil {
			logger.Logger.Error("Error getting underlying database:", err)
		}

		// 关闭 postgres 连接
		if err := db.Close(); err != nil {
			logger.Logger.Error("Error closing postgres:", err)
		}
	}

	if RDB != nil {
		// 关闭 redis 连接
		if err := RDB.Close(); err != nil {
			logger.Logger.Error("Error closing redis:", err)
		}
	}
}
