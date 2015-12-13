-- Based on DawsonG Love2D tutorial
-- https://github.com/DawsonG/Love2d-Tutorial-Scrolling-Shooter

loveframes = require("loveframes")

-- some useful globals here
debug = true
magic = {bulletMargin = 4, enemyMargin = 20, enemyRotate = math.pi,
  restartXMargin = 50, restartYMargin = 10,
  startPlayerX = 200, startPlayerY = 500,
  scoreX = 400, scoreY = 10}
player = {img = nil, x = magic.startPlayerX, y = magic.startPlayerY, speed = 250}
gun = {canShoot = true, canShootTimerMax = 0.2,
  canShootTimer = nil, bullet = nil, speed = 350, sound = nil}
bullets = { }
enemyRes = {makeTimerMax = 1., makeTimer = nil,
  img = nil, speed = 200}
enemies = { }
game = {isAlive = true, score = 0, hits = 0}

function collide(enemy, other)
  -- we rotate enemy pic on draw,
  -- so we should check collide against
  -- rotated pic
  local rotatedX = enemy.x - enemy.img:getWidth()
  local rotatedY = enemy.y - enemy.img:getHeight()
  if
    enemy.x < other.x or
    other.x + other.img:getWidth() < rotatedX or
    enemy.y < other.y or
    other.y + other.img:getHeight() < rotatedY then
    return false
  end
  return true
end

function love.load()
  --
  player.img = love.graphics.newImage('assets/images/aircraft_1.png')
  --
  gun.canShootTimer = gun.canShootTimerMax
  gun.bullet = love.graphics.newImage('assets/bullet.png')
  gun.sound = love.audio.newSource('assets/sounds/gun-sound.wav', 'static')
  --
  enemyRes.makeTimer = enemyRes.makeTimerMax
  enemyRes.img = love.graphics.newImage('assets/images/aircraft_1b.png')
  --
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
    local newBullet = {x = player.x + player.img:getWidth() / 2 - magic.bulletMargin, y = player.y,
      img = gun.bullet}
    table.insert(bullets, newBullet)
    gun.sound:play()
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
    local rnd = math.random(magic.enemyMargin, love.graphics.getWidth() - magic.enemyMargin)
    local newEnemy = {img = enemyRes.img, x = rnd, y = -magic.enemyMargin}
    table.insert(enemies, newEnemy)
  end
  for k, enemy in pairs(enemies) do
    enemy.y = enemy.y + enemyRes.speed * dt
    if enemy.y > love.graphics.getHeight() + magic.enemyMargin then
      table.remove(enemies, k)
    end
  end
  -- check collisions
  for i, enemy in pairs(enemies) do
    for j, bullet in pairs(bullets) do
      if collide(enemy, bullet) then
        table.remove(enemies, i)
        table.remove(bullets, j)
        game.score = game.score + 1
     end
    end
    if collide(enemy, player) and game.isAlive then
      table.remove(enemies, i)
      game.isAlive = false
    end
  end
  --
  if not game.isAlive and love.keyboard.isDown('r') then
    bullets = { }
    enemies = { }
    gun.canShoot = true
    gun.canShootTimer = gun.canShootTimerMax
    player.x = magic.startPlayerX
    player.y = magic.startPlayerY
    game.score = 0
    game.isAlive = true
  end
  -- gui stuff
  loveframes.update(dt)
end

function love.draw()
  if game.isAlive then
    love.graphics.draw(player.img, player.x, player.y)
  else
    love.graphics.print(
      'Press \'R\' to restart',
      love.graphics:getWidth() / 2 - magic.restartXMargin,
      love.graphics:getHeight() / 2 - magic.restartYMargin
    )
  end

  for k, bullet in pairs(bullets) do
    love.graphics.draw(bullet.img, bullet.x, bullet.y)
  end

  for k, enemy in pairs(enemies) do
    love.graphics.draw(enemy.img, enemy.x, enemy.y, magic.enemyRotate)
  end

  love.graphics.setColor(255, 255, 255)
  love.graphics.print('Score: ' .. tostring(game.score), magic.scoreX, magic.scoreY)
  --
  loveframes.draw()
end

function love.textinput(text)
  loveframes.textinput(text)
end
