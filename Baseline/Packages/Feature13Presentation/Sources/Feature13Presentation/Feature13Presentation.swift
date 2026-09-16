import Feature13Domain
import Feature13Data

public enum Feature13PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature13DomainModel = Feature13DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
