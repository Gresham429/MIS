window.onload = function () {
    // 初始化 "Particles" 插件
    var particlesConfig = {
        selector: "#Canvas", // 你的 canvas 元素的 CSS 选择器
        maxParticles: 300, // 粒子的最大数量
        sizeVariations: 3, // 粒子大小的变化量
        speed: 0.5, // 粒子的移动速度
        color: [
            "#FFD700", // 金色
            "#FF8C00", // 橙色
            "#7FFF00", // 鹦鹉绿
            "#FF00FF", // 紫红色
            "#FFFF00", // 黄色
            "#00FF00", // 酸橙色
            "#FF1493", // 深粉色
            "#00BFFF", // 深天蓝
            "#FF4500", // 番茄红
            "#FFA500", // 橙色
            "#00FFFF", // 青色
            "#FFC0CB", // 粉红色
            "#FFFFE0", // 浅黄色
            "#F0E68C", // 卡其色
            "#F08080", // 淡珊瑚色
        ],
        // 粒子和连接线的颜色，也可以是一个包含多个颜色的数组
        minDistance: 80, // 连接线的最小距离（像素）
        connectParticles: true, // 是否绘制连接线，true 表示绘制连接线，false 表示不绘制连接线
        responsive: [
            // 响应式配置，根据不同的屏幕宽度应用不同的配置
            {
                breakpoint: 768, // 屏幕宽度小于等于 768px 时应用的配置
                options: {
                    maxParticles: 50,
                    speed: 0.3,
                },
            },
            {
                breakpoint: 480, // 屏幕宽度小于等于 480px 时应用的配置
                options: {
                    maxParticles: 30,
                    speed: 0.2,
                },
            },
        ],
    };
    Particles.init(particlesConfig);
};