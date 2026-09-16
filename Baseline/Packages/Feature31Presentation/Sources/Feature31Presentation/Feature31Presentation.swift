import Feature31Domain
import Feature31Data

public enum Feature31PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature31DomainModel = Feature31DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
