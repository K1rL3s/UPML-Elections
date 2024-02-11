import { isVoteDisplayShown } from "src/store/MainStore/getters";

export function login(state, sessionId) {
  state.sessionId = sessionId;
}
