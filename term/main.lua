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
startImgFiles = {
  'assets/images/aircraft_1b.png',
  'assets/images/aircraft_1b.png',
  'assets/images/aircraft_1c.png',
  'assets/images/aircraft_1d.png',
  'assets/images/aircraft_1e.png',
  'assets/images/aircraft_2b.png',
  'assets/images/aircraft_2c.png',
  'assets/images/aircraft_2d.png',
  'assets/images/aircraft_2e.png',
  'assets/images/aircraft_3b.png',
  'assets/images/aircraft_3d.png',
  'assets/images/aircraft_3e.png'
}

lightImgFiles = {
  'assets/images/aircraft_1b_hit.png',
  'assets/images/aircraft_1c_hit.png',
  'assets/images/aircraft_1d_hit.png',
  'assets/images/aircraft_1e_hit.png',
  'assets/images/aircraft_2b_hit.png',
  'assets/images/aircraft_2c_hit.png',
  'assets/images/aircraft_2d_hit.png',
  'assets/images/aircraft_2e_hit.png',
  'assets/images/aircraft_3b_hit.png',
  'assets/images/aircraft_3d_hit.png',
  'assets/images/aircraft_3e_hit.png'
}

hitImgFiles = {
  'assets/images/aircraft_1b_destroyed.png',
  'assets/images/aircraft_1c_destroyed.png',
  'assets/images/aircraft_1d_destroyed.png',
  'assets/images/aircraft_1e_destroyed.png',
  'assets/images/aircraft_2b_destroyed.png',
  'assets/images/aircraft_2c_destroyed.png',
  'assets/images/aircraft_2d_destroyed.png',
  'assets/images/aircraft_2e_destroyed.png',
  'assets/images/aircraft_3b_destroyed.png',
  'assets/images/aircraft_3d_destroyed.png',
  'assets/images/aircraft_3e_destroyed.png'
}

enemyRes = {makeTimerMax = 1., makeTimer = nil,
  startImgs = {}, lightImgs = {}, hitImgs = {}, speed = 200, hitMax = 1, lightMax = 0.5}
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
  for k, img in pairs(startImgFiles) do
    table.insert(enemyRes.startImgs, love.graphics.newImage(img))
  end
  for k, img in pairs(lightImgFiles) do
    table.insert(enemyRes.lightImgs, love.graphics.newImage(img))
  end
  for k, img in pairs(hitImgFiles) do
    table.insert(enemyRes.hitImgs, love.graphics.newImage(img))
  end
  --
  loveframes.SetState('startMenu')
  showStartMenu()
end

function showStartMenu()
  local margin = 30
  --
  local play = loveframes.Create('button')
  play:SetText('Play')
  play:SetPos(
    love.graphics.getWidth() / 2 - margin,
    love.graphics.getHeight() / 2
  )
  play:SetState('startMenu')
  play.OnClick = function(object)
    loveframes.SetState('none')
  end
  --
  local exit = loveframes.Create('button')
  exit:SetText('Exit')
  exit:SetPos(
    love.graphics.getWidth() / 2 - margin,
    love.graphics.getHeight() / 2 + margin
  )
  exit:SetState('startMenu')
  exit.OnClick = function(object)
    love.event.push('quit')
  end
end

function restartGame()
  bullets = { }
  enemies = { }
  gun.canShoot = true
  gun.canShootTimer = gun.canShootTimerMax
  player.x = magic.startPlayerX
  player.y = magic.startPlayerY
  game.score = 0
  game.hits = 0
  game.isAlive = true
end

function showPauseMenu()
  local margin = 30
  --
  local resume = loveframes.Create('button')
  resume:SetText('Resume')
  resume:SetPos(
    love.graphics.getWidth() / 2 - margin,
    love.graphics.getHeight() / 2
  )
  resume:SetState('pauseMenu')
  resume.OnClick = function(object)
    loveframes.SetState('none')
  end
  --
  local restart = loveframes.Create('button')
  restart:SetText('Restart')
  restart:SetPos(
    love.graphics.getWidth() / 2 - margin,
    love.graphics.getHeight() / 2 + margin
  )
  restart:SetState('pauseMenu')
  restart.OnClick = function(object)
    restartGame()
    loveframes.SetState('none')
  end
  --
  local exit = loveframes.Create('button')
  exit:SetText('Exit')
  exit:SetPos(
    love.graphics.getWidth() / 2 - margin,
    love.graphics.getHeight() / 2 + 2 * margin
  )
  exit:SetState('pauseMenu')
  exit.OnClick = function(object)
    love.event.push('quit')
  end
end

function updatePlayer(dt)
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
end

function updateShooter(dt)
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
end

function updateBullets(dt)
  for k, bullet in pairs(bullets) do
    bullet.y = bullet.y - gun.speed * dt
    if bullet.y < 0 then
      table.remove(bullets, k)
    end
  end
end

function updateEnemies(dt)
  enemyRes.makeTimer = enemyRes.makeTimer - dt
  if enemyRes.makeTimer < 0 then
    enemyRes.makeTimer = enemyRes.makeTimerMax
    local rnd = math.random(magic.enemyMargin, love.graphics.getWidth() - magic.enemyMargin)
    local imgPos = math.random(1, #enemyRes.startImgs - 1)
    local newEnemy = {img = enemyRes.startImgs[imgPos], x = rnd, y = -magic.enemyMargin,
      hit = 0, imgNum = imgPos, isLight = false, sumLight = 0}
    table.insert(enemies, newEnemy)
  end
  for k, enemy in pairs(enemies) do
    enemy.y = enemy.y + enemyRes.speed * dt
    if enemy.isLight then
      enemy.sumLight = enemy.sumLight + dt
      if enemy.sumLight > enemyRes.lightMax then
        enemy.sumLight = 0
        enemy.isLight = false
        enemy.img = enemyRes.hitImgs[enemy.imgNum]
      end
    end
    if enemy.y > love.graphics.getHeight() + magic.enemyMargin then
      table.remove(enemies, k)
    end
    if enemy.hit > enemyRes.hitMax then
      game.score = game.score + 1
      table.remove(enemies, k)
    end
  end
end

function hitEnemy(enemy, dt)
  enemy.isLight = true
  enemy.hit = enemy.hit + 1
  enemy.img = enemyRes.lightImgs[enemy.imgNum]
  enemy.sumLight = dt
end

function updateCollisions(dt)
  for i, enemy in pairs(enemies) do
    for j, bullet in pairs(bullets) do
      if collide(enemy, bullet) then
        hitEnemy(enemy, dt)
        table.remove(bullets, j)
        game.hits = game.hits + 1
      end
    end
    if collide(enemy, player) and game.isAlive then
      table.remove(enemies, i)
      game.isAlive = false
    end
  end
end

function love.update(dt)
  if love.keyboard.isDown('escape') then
    loveframes.SetState('pauseMenu')
    showPauseMenu()
  end

  if loveframes.GetState() == 'none' then
    updatePlayer(dt)
    updateShooter(dt)
    updateBullets(dt)
    updateEnemies(dt)
    updateCollisions(dt)
    if not game.isAlive and love.keyboard.isDown('r') then
      restartGame()
    end
  end
  -- gui stuff
  loveframes.update(dt)
end

function drawPlayer()
  if game.isAlive then
    love.graphics.draw(player.img, player.x, player.y)
  else
    love.graphics.print(
      'Press \'R\' to restart',
      love.graphics:getWidth() / 2 - magic.restartXMargin,
      love.graphics:getHeight() / 2 - magic.restartYMargin
    )
  end
end

function drawBullets()
  for k, bullet in pairs(bullets) do
    love.graphics.draw(bullet.img, bullet.x, bullet.y)
  end
end

function drawEnemies()
  for k, enemy in pairs(enemies) do
    love.graphics.draw(enemy.img, enemy.x, enemy.y, magic.enemyRotate)
  end
end

function drawScore()
  love.graphics.setColor(255, 255, 255)
  love.graphics.print('Score: ' .. tostring(game.score), magic.scoreX, magic.scoreY)
  love.graphics.print('Hits: ' .. tostring(game.hits), magic.scoreX, magic.scoreY + 20)
end

function love.draw()
  if loveframes.GetState() == 'none' then
    drawPlayer()
    drawBullets()
    drawEnemies()
    drawScore()
  end
  loveframes.draw()
end

function love.mousepressed(x, y, button)
  loveframes.mousepressed(x, y, button)
end

function love.mousereleased(x, y, button)
  loveframes.mousereleased(x, y, button)
end

function love.keypressed(key, unicode)
  loveframes.keypressed(key, unicode)
end

function love.keyreleased(key)
  loveframes.keyreleased(key)
end

function love.textinput(text)
  loveframes.textinput(text)
end
