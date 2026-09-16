import Feature17Domain
import Feature17Data

public enum Feature17PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature17DomainModel = Feature17DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
