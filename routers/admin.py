from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import *
from aiogram.types import ContentType as CT
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.exceptions import TelegramForbiddenError

from create_bot import logger, bot
from utility.filters import AllowedUsers
from utility.template_images import change_image
from utility.MediaGroupMiddleware import MediaGroupMiddleware

from logic.core import *
from logic.admin import *
from messages import admin as messages
from keyboards import admin as keyboards

 
router = Router(name='admin')
router.message.filter(AllowedUsers())
router.message.middleware(MediaGroupMiddleware())

class AnnounceStates(StatesGroup):
    approve = State()


@router.message(CommandStart())
async def message_start(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)

    data = await state.get_data()

    await get_stats_data()

    await message.answer(
        text=messages.start(lang, user),
        reply_markup=keyboards.start(lang)
    )

    for key in data.keys():
        try: 
            if 'id' in key: 
                await bot.delete_message(user.id, data[key])
        except: pass
    await state.set_data({})
    await state.clear()
 
    logger.info(f'@{user.username} admin_id [{user.id}] started bot')


@router.callback_query(F.data == 'start')
async def query_start(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    data = await state.get_data()

    await query.message.answer(
        text=messages.start(lang, user),
        reply_markup=keyboards.start(lang)
    )

    for key in data.keys():
        try:
            if 'id' in key:
                await bot.delete_message(user.id, data[key])
        except: pass

    try:
        await query.message.delete()
    except:
        pass

    await state.set_data({})
    await state.clear()

    logger.info(f'@{user.username} admin_id [{user.id}] called start')


@router.callback_query(F.data == 'stats')
async def query_stats(query: CallbackQuery):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    data = await get_stats_data()

    await query.message.edit_text(
        text=messages.stats(lang, data),
        reply_markup=keyboards.go_back(lang)
    )
    
    logger.info(f'@{user.username} admin_id [{user.id}] called stats')


@router.message(F.caption == '/add_image_vinyl', F.photo)
async def message_add_image_templates_vinyl(message: Message):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    file_id = message.photo[-1].file_id

    change_image('templates_vinyl', file_id)

    await message.answer(
        text=messages.vinyl_template(lang)
    )

    logger.info(f'@{user.username} admin_id [{user.id}] changed vinyl template image')


@router.message(F.caption == '/add_image_album', F.photo)
async def message_add_image_templates_album(message: Message):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    file_id = message.photo[-1].file_id

    change_image('templates_album', file_id)

    await message.answer(
        text=messages.album_template(lang)
    )

    logger.info(f'@{user.username} admin_id [{user.id}] changed albums template image')


@router.message(F.caption == '/add_image_player', F.photo)
async def message_add_image_templates_album(message: Message):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    file_id = message.photo[-1].file_id

    change_image('templates_player', file_id)

    await message.answer(
        text=messages.player_template(lang)
    )

    logger.info(f'@{user.username} admin_id [{user.id}] changed player template image')


@router.message(F.text.startswith('/add_image_'))
async def message_add_image_help(message: Message):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)

    await message.answer(
        text=messages.add_image_help(lang, message.text.replace('/', '\/')),
        parse_mode='MarkdownV2'
    )
    
    logger.info(f'@{user.username} admin_id [{user.id}] tried to use {message.text}')


@router.message(F.text.startswith('/announce'))
async def message_announce_try(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)

    if len(message.text.replace('/announce', '').strip()) == 0:
        await message.answer(
            text=messages.announcement_help(lang),
            parse_mode='MarkdownV2'
        )
    else:
        mtd_1 = await message.answer(
            text=messages.announcement_approve_1(lang)
        )
        mtd_2 = await message.answer(
            text=message.html_text.replace('/announce\n', ''),
            parse_mode='HTML'
        )
        mtd_3 = await message.answer(
            text=messages.announcement_approve_2(lang),
            reply_markup=keyboards.announcement(lang),
            parse_mode='MarkdownV2'
        )

        await state.set_data(
            {
                'message': message.html_text.replace('/announce', ''),
                'to_delete': [mtd_1.message_id, mtd_2.message_id, mtd_3.message_id]
            }
        )
        await state.set_state(AnnounceStates.approve)

    logger.info(f'@{user.username} admin_id [{user.id}] used /announce')


@router.message(StateFilter(None), F.content_type.in_([CT.PHOTO, CT.VIDEO, CT.AUDIO, CT.DOCUMENT, CT.ANIMATION]))
async def media_announce_try(message: Message, state: FSMContext, media_group: list[Message] | None):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)

    if '/announce' not in message.caption: return 

    if len(message.caption.replace('/announce', '').strip()) == 0:
        await message.answer(
            text=messages.announcement_help(lang),
            parse_mode='MarkdownV2'
        )
    elif media_group is None:
        mtd_1 = await message.answer(text=messages.announcement_approve_1(lang))
        if message.photo:
            ft = 'photo'
            fid = message.photo[-1].file_id
            mtd_2 = await message.answer_photo(
                photo=fid,
                caption=message.html_text.replace('/announce\n', ''),
                parse_mode='HTML'
            )
        elif message.video:
            ft = 'video'
            fid = message.video.file_id
            mtd_2 = await message.answer_video(
                video=fid,
                caption=message.html_text.replace('/announce\n', ''),
                parse_mode='HTML'
            )
        elif message.document:
            ft = 'document'
            fid = message.document.file_id
            mtd_2 = await message.answer_document(
                document=fid,
                caption=message.html_text.replace('/announce\n', ''),
                parse_mode='HTML'
            )
        elif message.animation:
            ft = 'animation'
            fid = message.animation.file_id
            mtd_2 = await message.answer_animation(
                animation=fid,
                caption=message.html_text.replace('/announce\n', ''),
                parse_mode='HTML'
            )
        elif message.audio:
            ft = 'audio'
            fid = message.audio.file_id
            mtd_2 = await message.answer_audio(
                audio=fid,
                caption=message.html_text.replace('/announce\n', ''),
                parse_mode='HTML'
            )
        mtd_3 = await message.answer(
            text=messages.announcement_approve_2(lang),
            reply_markup=keyboards.announcement(lang),
            parse_mode='MarkdownV2'
        )

        await state.set_data(
            {
                'message': message.html_text.replace('/announce', ''),
                'to_delete': [mtd_1.message_id, mtd_2.message_id, mtd_3.message_id],
                'file_type': ft, 'file_id': fid
            }
        )
        await state.set_state(AnnounceStates.approve)
    else:
        media_group_here = []
        try:
            for msg in media_group:
                if msg.photo:
                    file_id = msg.photo[-1].file_id
                    media_group_here.append(InputMediaPhoto(media=file_id))
                elif msg.video:
                    file_id = msg.video.file_id
                    media_group_here.append(InputMediaVideo(media=file_id))
                elif msg.audio:
                    file_id = msg.audio.file_id
                    media_group_here.append(InputMediaAudio(media=file_id))
                elif msg.document:
                    file_id = msg.document.file_id
                    media_group_here.append(InputMediaDocument(media=file_id))
                elif msg.animation:
                    file_id = msg.animation.file_id
                    media_group_here.append(InputMediaAnimation(media=file_id))
        except Exception as e:
            print(e)

        media_group_here[0].caption = message.html_text.replace('/announce\n', '')
        media_group_here[0].parse_mode='HTML'

        mtd_1 = await message.answer(text=messages.announcement_approve_1(lang))
        mtd_2 = await message.answer_media_group( media=media_group_here)
        mtd_3 = await message.answer(
            text=messages.announcement_approve_2(lang),
            reply_markup=keyboards.announcement(lang),
            parse_mode='MarkdownV2'
        )

        await state.set_data(
            {
                'message': message.html_text.replace('/announce', ''),
                'to_delete': [mtd_1.message_id, mtd_3.message_id] + [x.message_id for x in mtd_2],
                'media_group': media_group_here
            }
        )
        await state.set_state(AnnounceStates.approve)

    logger.info(f'@{user.username} admin_id [{user.id}] used /announce')


@router.callback_query(F.data == 'announce')
async def announce_approve(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    if state is None:
        await query.answer('Failure, try again ❌', show_alert=True)
        return

    data = await state.get_data()
    message = data['message']

    for m in data['to_delete']:
        try: await bot.delete_message(user.id, m)
        except: pass

    mtd = await query.message.answer(
        text=messages.announce_start(lang),
    )

    users = await get_all_users()

    logger.info('Announcement started')

    for u in users:
        u = u[0]
        if u.id == user.id: continue
        try:
            if 'media_group' in data.keys():
                await bot.send_media_group(u.id, media=data['media_group'])
            elif 'file_type' in data.keys():
                match data['file_type']:
                    case 'photo':
                        await bot.send_photo(u.id, photo=data['file_id'], caption=message, parse_mode='HTML')
                    case 'video':
                        await bot.send_video(u.id, video=data['file_id'], caption=message, parse_mode='HTML')
                    case 'document':
                        await bot.send_document(u.id, document=data['file_id'], caption=message, parse_mode='HTML')
                    case 'audio':
                        await bot.send_audio(u.id, audio=data['file_id'], caption=message, parse_mode='HTML')
                    case 'animation':
                        await bot.send_animation(u.id, animation=data['file_id'], caption=message, parse_mode='HTML')
            else:
                await bot.send_message(u.id, text=message, parse_mode='HTML')
            logger.info(f'@{u.username} received announcement from @{user.username} admin_id [{user.id}]')
        except TelegramForbiddenError:
            await set_blocked(u)
        except Exception as e:
            print('SOME EXCEPTION ON ANNOUNCEMENT', e)

    try:
        await bot.delete_message(user.id, mtd.message_id)
    except: pass
    await query.message.answer(
        text=messages.announce_end(lang),
        reply_markup=keyboards.go_back(lang)
    )

    logger.info('Announcement finished')
