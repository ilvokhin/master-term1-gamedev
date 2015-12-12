-- Based on DawsonG Love2D tutorial
-- https://github.com/DawsonG/Love2d-Tutorial-Scrolling-Shooter

-- some useful globals here
debug = true
player = {img = nil, x = 200, y = 500, speed = 250}
gun = {canShoot = true, canShootTimerMax = 0.2,
  canShootTimer = nil, bullet = nil, speed = 350}
bullets = { }
magic = {bulletMargin = 4, enemyMargin = 20, enemyRotate = math.pi}
enemyRes = {makeTimerMax = 0.4, makeTimer = nil,
  img = nil, speed = 200}
enemies = { }

function love.load()
  --
  player.img = love.graphics.newImage('assets/images/aircraft_1.png')
  --
  gun.canShootTimer = gun.canShootTimerMax
  gun.bullet = love.graphics.newImage('assets/bullet.png')
  --
  enemyRes.makeTimer = enemyRes.makeTimerMax
  enemyRes.img = love.graphics.newImage('assets/images/aircraft_1b.png')
end

function love.update(dt)
  if love.keyboard.isDown('escape') then
    love.event.push('quit')
  end

  if love.keyboard.isDown('left', 'a') then
    if player.x > 0 then
      player.x = player.x - player.speed * dt
    end
  elseif love.keyboard.isDown('right', 'd') then
    if player.x < love.graphics.getWidth() - player.img:getWidth() then
      player.x = player.x + player.speed * dt
    end
  elseif love.keyboard.isDown('up', 'w') then
    if player.y > 0 then
      player.y = player.y - player.speed * dt
    end
  elseif love.keyboard.isDown('down', 's') then
    if player.y < love.graphics.getHeight() - player.img:getHeight() then
      player.y = player.y + player.speed * dt
    end
  end

  gun.canShootTimer = gun.canShootTimer - dt
  if gun.canShootTimer < 0 then
    gun.canShoot = true
  end

  if love.keyboard.isDown(' ', 'rctrl', 'lctrl', 'ctrl') and gun.canShoot then
    newBullet = {x = player.x + player.img:getWidth() / 2 - magic.bulletMargin, y = player.y,
      img = gun.bullet}
    table.insert(bullets, newBullet)
    gun.canShoot = false
    gun.canShootTimer = gun.canShootTimerMax
  end

  for k, bullet in pairs(bullets) do
    bullet.y = bullet.y - gun.speed * dt
    if bullet.y < 0 then
      table.remove(bullets, k)
    end
  end
  --
  enemyRes.makeTimer = enemyRes.makeTimer - dt
  if enemyRes.makeTimer < 0 then
    enemyRes.makeTimer = enemyRes.makeTimerMax
    rnd = math.random(magic.enemyMargin, love.graphics.getWidth() - magic.enemyMargin)
    newEnemy = {img = enemyRes.img, x = rnd, y = -magic.enemyMargin}
    table.insert(enemies, newEnemy)
  end
  for k, enemy in pairs(enemies) do
    enemy.y = enemy.y + enemyRes.speed * dt
    if enemy.y > love.graphics.getHeight() + magic.enemyMargin then
      table.remove(enemies, k)
    end
  end
end

function love.draw(dt)
  love.graphics.draw(player.img, player.x, player.y)

  for k, bullet in pairs(bullets) do
    love.graphics.draw(bullet.img, bullet.x, bullet.y)
  end

  for k, enemy in pairs(enemies) do
    love.graphics.draw(enemy.img, enemy.x, enemy.y, magic.enemyRotate)
  end
end
